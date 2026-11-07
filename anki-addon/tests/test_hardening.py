"""
Regression tests for the security hardening and theme fixes:
- HTTP bridge authentication / host checks
- HTML escaping of untrusted card text
- SSRF guard for image downloads
- Color helpers, accent application, hex validation
"""

import os
import socket
import sys
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import config
from discord.client import HttpBridgeServer, discord_client_manager
from anki.media import UnsafeURLError, _assert_public_url
from anki.notes import _format_markdown_to_anki_html
from theme.palette import contrast_ratio, is_valid_hex, mix, normalize_hex, readable_text_on, with_alpha
from theme.styles import generate_qss, generate_webview_css


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class TestHttpBridgeSecurity(unittest.TestCase):
    def setUp(self):
        self._saved_token = config.get("discord.secret_token", "")
        self.port = _free_port()
        self.server = HttpBridgeServer(host="127.0.0.1", port=self.port)
        self.assertTrue(self.server.start())

    def tearDown(self):
        self.server.stop()
        config.set("discord.secret_token", self._saved_token, save=False)

    def _post(self, headers=None, host=None):
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/api/card",
            data=b'{"content": "hello"}',
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        if host:
            req.add_header("Host", host)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, resp.headers
        except urllib.error.HTTPError as e:
            return e.code, e.headers

    def test_locked_without_configured_token(self):
        config.set("discord.secret_token", "", save=False)
        status, _ = self._post({"Authorization": "Bearer anything"})
        self.assertEqual(status, 503)

    def test_rejects_missing_or_wrong_token(self):
        config.set("discord.secret_token", "s3cret", save=False)
        self.assertEqual(self._post()[0], 401)
        self.assertEqual(self._post({"Authorization": "Bearer wrong"})[0], 401)

    def test_rejects_foreign_host_header(self):
        config.set("discord.secret_token", "s3cret", save=False)
        status, _ = self._post({"Authorization": "Bearer s3cret"}, host="evil.example.com")
        self.assertEqual(status, 403)

    def test_accepts_valid_token_and_sends_no_cors(self):
        config.set("discord.secret_token", "s3cret", save=False)
        for headers in ({"Authorization": "Bearer s3cret"}, {"X-AWT-Token": "s3cret"}):
            status, resp_headers = self._post(headers)
            # 400 = authenticated, but "hello" is not a valid !anki card
            self.assertEqual(status, 400)
            self.assertIsNone(resp_headers.get("Access-Control-Allow-Origin"))


class TestBridgeDefaults(unittest.TestCase):
    def test_bridge_disabled_by_default(self):
        from core.config import DEFAULT_CONFIG
        self.assertFalse(DEFAULT_CONFIG["discord"]["http_bridge_enabled"])

    def test_client_manager_has_shutdown(self):
        discord_client_manager.shutdown()  # must not raise


class TestHtmlEscaping(unittest.TestCase):
    def test_raw_html_is_escaped(self):
        out = _format_markdown_to_anki_html('<img src=x onerror="alert(1)"> **bold**')
        self.assertNotIn("<img", out)
        self.assertIn("&lt;img", out)
        self.assertIn("<b>bold</b>", out)

    def test_cloze_and_ampersand_preserved(self):
        out = _format_markdown_to_anki_html("{{c1::Tokyo}} & Kyoto")
        self.assertIn("{{c1::Tokyo}}", out)
        self.assertIn("&amp;", out)


class TestSsrfGuard(unittest.TestCase):
    def test_blocks_internal_addresses(self):
        for url in ("http://127.0.0.1/a.png", "http://localhost/a.png", "http://10.0.0.5/a.png",
                    "http://192.168.1.1/a.png", "http://169.254.169.254/latest", "ftp://example.com/a.png"):
            with self.assertRaises(UnsafeURLError, msg=url):
                _assert_public_url(url)


class TestColorHelpers(unittest.TestCase):
    def test_hex_validation(self):
        self.assertTrue(is_valid_hex("#000"))
        self.assertTrue(is_valid_hex("#0a84ff"))
        self.assertFalse(is_valid_hex("#zzz"))
        self.assertFalse(is_valid_hex("0A84FF"))
        self.assertFalse(is_valid_hex("#12345"))
        self.assertEqual(normalize_hex("#abc"), "#AABBCC")
        self.assertEqual(normalize_hex("#zzz", "#111111"), "#111111")
        self.assertEqual(normalize_hex(None, "#222222"), "#222222")

    def test_contrast_and_readable_text(self):
        self.assertAlmostEqual(contrast_ratio("#000000", "#FFFFFF"), 21.0, places=1)
        self.assertEqual(readable_text_on("#FFFFFF"), "#000000")
        self.assertEqual(readable_text_on("#000000"), "#FFFFFF")
        self.assertEqual(mix("#000000", "#FFFFFF", 0.5), "#808080")
        self.assertEqual(with_alpha("#0A84FF", 0.5), "rgba(10, 132, 255, 0.50)")


class TestAccentIsApplied(unittest.TestCase):
    def test_accent_drives_qss(self):
        qss = generate_qss(accent="#FF3366", bg_color="#000000")
        self.assertIn("#FF3366", qss)  # primary buttons / checked checkbox / focus border
        self.assertIn("rgba(255, 51, 102", qss)  # selection highlight

    def test_accent_drives_webview_links(self):
        css = generate_webview_css(accent="#FF3366", bg_color="#000000")
        self.assertIn("--accent: #FF3366", css)
        self.assertIn("color: #FF3366 !important", css)

    def test_low_contrast_accent_is_adjusted_for_text(self):
        # Black accent on black background would be invisible as link text
        css = generate_webview_css(accent="#000000", bg_color="#000000")
        self.assertNotIn("--link: #000000", css)

    def test_invalid_colors_fall_back(self):
        qss = generate_qss(accent="#zzz", bg_color="not-a-color")
        self.assertIn("background-color: #000000", qss)


if __name__ == "__main__":
    unittest.main()
