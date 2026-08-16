"""
Unit tests for Discord Image Ingestion Pipeline and MediaManager.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anki.media import MediaManager, media_manager
from core.config import config
from discord.bridge import DiscordBridge
from discord.models import DiscordAttachment, DiscordChannel, DiscordMessageEvent, DiscordUser
from sync.queue import job_queue


class TestImageIngestion(unittest.TestCase):
    def setUp(self):
        self.bridge = DiscordBridge()
        job_queue.clear()
        config.reset_to_defaults()
        config.set("discord.image_channels", ["channel_img_123"], save=False)
        config.set("discord.image_default_deck", "Biology::Anatomy", save=False)
        config.set("discord.image_default_tags", ["anatomy", "discord"], save=False)

    def test_extract_extension(self):
        m = MediaManager()
        self.assertEqual(m._extract_extension("https://cdn.discord.com/a.png", "image/png"), "png")
        self.assertEqual(m._extract_extension("https://cdn.discord.com/b.jpg", "image/jpeg"), "jpg")
        self.assertEqual(m._extract_extension("https://cdn.discord.com/c.webp", ""), "webp")

    def test_image_channel_auto_ingestion(self):
        event = DiscordMessageEvent(
            id="msg_img_001",
            content="Heart Structure Diagram",
            author=DiscordUser(id="user_doc", name="Doctor"),
            channel=DiscordChannel(id="channel_img_123"),
            attachments=[
                DiscordAttachment(
                    id="att_1",
                    url="https://via.placeholder.com/150",
                    filename="heart.png",
                    content_type="image/png",
                )
            ],
        )

        # Mock download_and_save_image so tests don't require internet connectivity
        original_download = media_manager.download_and_save_image
        media_manager.download_and_save_image = lambda url, fn=None: (True, "discord_mock12345.png", "mockhash123")

        try:
            success, reply = self.bridge.handle_incoming_message("", event)
            self.assertTrue(success)
            self.assertIn("enqueued 1 image flashcard", reply)

            # Check enqueued job
            self.assertEqual(job_queue.get_pending_count(), 1)
            job = job_queue.get_next()
            self.assertIsNotNone(job)
            self.assertIn('<img src="discord_mock12345.png">', job.payload.front)
            self.assertEqual(job.payload.deck, "Biology::Anatomy")
            self.assertEqual(job.payload.tags, ["anatomy", "discord"])

        finally:
            media_manager.download_and_save_image = original_download

    def test_image_back_layout(self):
        config.set("discord.image_card_layout", "image_back", save=False)
        event = DiscordMessageEvent(
            id="msg_img_002",
            content="Identify this muscle",
            author=DiscordUser(id="user_doc", name="Doctor"),
            channel=DiscordChannel(id="channel_img_123"),
            attachments=[
                DiscordAttachment(
                    id="att_2",
                    url="https://via.placeholder.com/150",
                    filename="muscle.png",
                )
            ],
        )

        original_download = media_manager.download_and_save_image
        media_manager.download_and_save_image = lambda url, fn=None: (True, "discord_muscle.png", "mockhash456")

        try:
            success, reply = self.bridge.handle_incoming_message("Identify this muscle", event)
            self.assertTrue(success)

            job = job_queue.get_next()
            self.assertIsNotNone(job)
            self.assertEqual(job.payload.front, "Identify this muscle")
            self.assertIn('<img src="discord_muscle.png">', job.payload.back)

        finally:
            media_manager.download_and_save_image = original_download

    def test_image_only_front_layout(self):
        config.set("discord.image_card_layout", "image_only_front", save=False)
        event = DiscordMessageEvent(
            id="msg_img_003",
            content="Some caption that should not appear on back",
            author=DiscordUser(id="user_doc", name="Doctor"),
            channel=DiscordChannel(id="channel_img_123"),
            attachments=[
                DiscordAttachment(
                    id="att_3",
                    url="https://via.placeholder.com/150",
                    filename="radiology.png",
                )
            ],
        )

        original_download = media_manager.download_and_save_image
        media_manager.download_and_save_image = lambda url, fn=None: (True, "discord_radiology.png", "mockhash789")

        try:
            success, reply = self.bridge.handle_incoming_message("", event)
            self.assertTrue(success)

            job = job_queue.get_next()
            self.assertIsNotNone(job)
            self.assertIn('<img src="discord_radiology.png">', job.payload.front)
            self.assertEqual(job.payload.back, "")

        finally:
            media_manager.download_and_save_image = original_download

    def test_image_optimization_toggle(self):
        m = MediaManager()
        raw_mock = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        
        # When optimize_images is disabled
        config.set("discord.optimize_images", False, save=False)
        data, ext, saved = m.optimize_image_data(raw_mock, "png")
        self.assertEqual(data, raw_mock)
        self.assertEqual(ext, "png")
        self.assertEqual(saved, 0)

    def test_gif_animation_preserved(self):
        m = MediaManager()
        raw_gif = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        data, ext, saved = m.optimize_image_data(raw_gif, "gif")
        self.assertEqual(ext, "gif")
        self.assertEqual(data, raw_gif)


if __name__ == "__main__":
    unittest.main()
