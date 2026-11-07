"""
End-to-end tests for the Discord image pipeline as used by a Pinterest → Discord
webhook automation: embeds, webhook authors, catch-up polling, retries, dedup,
image-only cards.
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import config
from discord.client import DiscordPollingWorker
from discord import api as discord_api
from anki.media import StagedImage, media_manager
from core.image_urls import download_candidates, extract_image_urls
from sync.dedup import dedup_registry
from sync.queue import job_queue
from sync.worker import sync_worker

CHANNEL = "555000111"
WEBHOOK_ID = "777000"


def webhook_msg(msg_id, image_url, content="", embed_type="rich", thumb_only=False):
    embed = {"type": embed_type}
    if thumb_only:
        embed["thumbnail"] = {"url": image_url}
    else:
        embed["image"] = {"url": image_url}
    return {
        "id": str(msg_id),
        "type": 0,
        "content": content,
        "webhook_id": WEBHOOK_ID,
        "author": {"id": WEBHOOK_ID, "username": "Pinterest", "bot": True},
        "attachments": [],
        "embeds": [embed],
    }


class FakeStager:
    """Replaces media_manager.stage_image: deterministic hashes, optional failures."""

    def __init__(self):
        self.calls = []
        self.fail_urls = set()

    def __call__(self, url):
        self.calls.append(url)
        if url in self.fail_urls:
            return StagedImage(False, error="HTTP Error 503")
        h = f"{abs(hash(url)):016x}"[:16]
        return StagedImage(True, filename=f"discord_{h}.webp", image_hash=h, source_url=url)


class DiscordImageBase(unittest.TestCase):
    def setUp(self):
        config.reset_to_defaults()
        config.set("discord.image_channels", [CHANNEL], save=False)
        config.set("discord.image_default_deck", "Pinterest::Mental", save=False)
        config.set("discord.image_default_tags", ["pinterest"], save=False)
        config.set("discord.rate_limit_per_minute", 5, save=False)
        job_queue.clear()
        dedup_registry.clear()

        self.stager = FakeStager()
        self._orig_stage = media_manager.stage_image
        media_manager.stage_image = self.stager

        self.tmpdir = tempfile.mkdtemp()
        self.poller = DiscordPollingWorker()
        self.poller._state_path = lambda: os.path.join(self.tmpdir, "state.json")
        self.poller._bot_user_id = "999999"

        self._orig_get_messages = discord_api.get_messages
        self.channel_messages = []

        def fake_get_messages(token, channel_id, after=None, before=None, limit=100):
            # Mirrors Discord: `after` returns the window right after the ID, `before`/none
            # the newest window; responses are always newest-first.
            msgs = sorted(self.channel_messages, key=lambda m: int(m["id"]))
            if after is not None:
                window = [m for m in msgs if int(m["id"]) > int(after)][:limit]
            else:
                if before is not None:
                    msgs = [m for m in msgs if int(m["id"]) < int(before)]
                window = msgs[-limit:]
            return list(reversed(window))

        discord_api.get_messages = fake_get_messages

    def tearDown(self):
        media_manager.stage_image = self._orig_stage
        discord_api.get_messages = self._orig_get_messages
        job_queue.clear()
        dedup_registry.clear()


class TestImageUrlExtraction(unittest.TestCase):
    def test_embed_image_thumbnail_attachment_and_link(self):
        msg = {
            "content": "look https://example.com/x.png",
            "attachments": [{"url": "https://cdn.discordapp.com/a.jpg", "content_type": "image/jpeg"},
                            {"url": "https://cdn.discordapp.com/doc.pdf", "content_type": "application/pdf"}],
            "embeds": [{"type": "rich", "image": {"url": "https://i.pinimg.com/736x/aa/bb/cc/1.jpg"},
                        "thumbnail": {"url": "https://i.pinimg.com/236x/aa/bb/cc/1.jpg"}},
                       {"type": "image", "thumbnail": {"url": "https://i.pinimg.com/236x/dd/ee/ff/2.jpg"}}],
        }
        self.assertEqual(extract_image_urls(msg), [
            "https://cdn.discordapp.com/a.jpg",
            "https://i.pinimg.com/736x/aa/bb/cc/1.jpg",
            "https://i.pinimg.com/236x/dd/ee/ff/2.jpg",
            "https://example.com/x.png",
        ])

    def test_pinterest_prefers_originals(self):
        self.assertEqual(download_candidates("https://i.pinimg.com/236x/aa/bb/cc/1.jpg"), [
            "https://i.pinimg.com/originals/aa/bb/cc/1.jpg",
            "https://i.pinimg.com/736x/aa/bb/cc/1.jpg",
            "https://i.pinimg.com/236x/aa/bb/cc/1.jpg",
        ])
        self.assertEqual(download_candidates("https://cdn.discordapp.com/a.png"), ["https://cdn.discordapp.com/a.png"])


class TestWebhookIngestion(DiscordImageBase):
    def test_webhook_embed_becomes_image_only_card(self):
        msg = webhook_msg(1001, "https://i.pinimg.com/736x/aa/bb/cc/1.jpg", content="My pin title <script>")
        self.assertEqual(self.poller.handle_message(CHANNEL, msg, "tok"), "ok")
        self.assertEqual(job_queue.get_pending_count(), 1)
        job = job_queue.get_all_jobs()[0]
        self.assertTrue(job.payload.front.startswith('<img src="discord_'))
        self.assertEqual(job.payload.back, "")  # image only, no back
        self.assertEqual(job.payload.deck, "Pinterest::Mental")
        self.assertEqual(job.payload.tags, ["pinterest"])

    def test_caption_layout_escapes_html(self):
        config.set("discord.image_card_layout", "image_front", save=False)
        msg = webhook_msg(1002, "https://i.pinimg.com/736x/aa/bb/cc/2.jpg", content="Title <img src=x onerror=1>")
        self.poller.handle_message(CHANNEL, msg, "tok")
        job = job_queue.get_all_jobs()[0]
        self.assertIn("&lt;img", job.payload.back)
        self.assertNotIn("<img src=x", job.payload.back)

    def test_thumbnail_only_embed_is_used(self):
        msg = webhook_msg(1003, "https://i.pinimg.com/236x/aa/bb/cc/3.jpg", embed_type="image", thumb_only=True)
        self.poller.handle_message(CHANNEL, msg, "tok")
        self.assertEqual(job_queue.get_pending_count(), 1)

    def test_own_bot_and_text_only_messages_are_ignored(self):
        own = webhook_msg(1004, "https://i.pinimg.com/736x/x/y/z/4.jpg")
        own.pop("webhook_id")
        own["author"] = {"id": "999999", "bot": True}
        self.poller.handle_message(CHANNEL, own, "tok")
        text_only = {"id": "1005", "type": 0, "content": "hello", "author": {"id": "1"}, "embeds": [], "attachments": []}
        self.poller.handle_message(CHANNEL, text_only, "tok")
        self.assertEqual(job_queue.get_pending_count(), 0)

    def test_burst_from_one_webhook_is_not_rate_limited(self):
        for i in range(20):  # rate limit set to 5/min in setUp
            self.poller.handle_message(CHANNEL, webhook_msg(2000 + i, f"https://i.pinimg.com/736x/a/b/c/{i}.jpg"), "tok")
        self.assertEqual(job_queue.get_pending_count(), 20)


class TestPollingCatchUp(DiscordImageBase):
    def test_first_poll_sets_baseline_then_imports_new_posts(self):
        self.channel_messages = [webhook_msg(100, "https://i.pinimg.com/736x/a/a/a/old.jpg")]
        self.poller.poll_channel(CHANNEL, "tok")
        self.assertEqual(job_queue.get_pending_count(), 0)  # history not imported automatically
        self.assertEqual(self.poller.get_last_id(CHANNEL), "100")

        # Posts made "while Anki was closed": more than one page worth
        self.channel_messages += [webhook_msg(200 + i, f"https://i.pinimg.com/736x/n/e/w/{i}.jpg") for i in range(150)]
        fresh = DiscordPollingWorker()  # new session: state comes from disk
        fresh._state_path = self.poller._state_path
        fresh._bot_user_id = "999999"
        handled = fresh.poll_channel(CHANNEL, "tok")
        self.assertEqual(handled, 150)
        self.assertEqual(job_queue.get_pending_count(), 150)
        self.assertEqual(fresh.get_last_id(CHANNEL), "349")

    def test_transient_download_failure_is_retried_then_skipped(self):
        self.channel_messages = [webhook_msg(100, "https://i.pinimg.com/736x/a/a/a/old.jpg")]
        self.poller.poll_channel(CHANNEL, "tok")
        bad = "https://i.pinimg.com/736x/b/a/d/bad.jpg"
        self.stager.fail_urls.add(bad)
        self.channel_messages += [webhook_msg(101, bad), webhook_msg(102, "https://i.pinimg.com/736x/g/o/o/d.jpg")]

        self.poller.poll_channel(CHANNEL, "tok")
        self.assertEqual(self.poller.get_last_id(CHANNEL), "100")  # not advanced past the failure
        self.poller.poll_channel(CHANNEL, "tok")
        self.assertEqual(self.poller.get_last_id(CHANNEL), "100")
        self.poller.poll_channel(CHANNEL, "tok")  # 3rd attempt: give up and move on
        self.assertEqual(self.poller.get_last_id(CHANNEL), "102")
        self.assertEqual(job_queue.get_pending_count(), 1)

    def test_import_history_backfills_and_skips_already_imported(self):
        self.channel_messages = [webhook_msg(300 + i, f"https://i.pinimg.com/736x/h/i/s/{i}.jpg") for i in range(30)]
        result = self.poller.import_history(CHANNEL, "tok", limit=1000)
        self.assertEqual(result["imported"], 30)
        sync_worker.process_all_pending()  # headless: creates notes synchronously
        again = self.poller.import_history(CHANNEL, "tok", limit=1000)
        self.assertEqual(again["imported"], 0)
        self.assertEqual(again["skipped"], 30)
        self.assertEqual(self.poller.get_last_id(CHANNEL), "329")


class TestWorkerDedup(DiscordImageBase):
    def test_same_image_in_two_messages_creates_one_card(self):
        url = "https://i.pinimg.com/736x/s/a/m/e.jpg"
        self.poller.handle_message(CHANNEL, webhook_msg(400, url), "tok")
        self.poller.handle_message(CHANNEL, webhook_msg(401, url), "tok")  # saved twice on Pinterest
        sync_worker.process_all_pending()
        stats = job_queue.get_stats()
        self.assertEqual(stats["success"], 1)
        self.assertEqual(stats["duplicate"], 1)


if __name__ == "__main__":
    unittest.main()
