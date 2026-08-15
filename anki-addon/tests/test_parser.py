"""
Unit tests for DiscordParser.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.exceptions import ParserError
from discord.models import DiscordChannel, DiscordMessageEvent, DiscordUser
from discord.parser import DiscordParser


class TestDiscordParser(unittest.TestCase):
    def setUp(self):
        self.parser = DiscordParser()

    def test_parse_valid_basic_message(self):
        raw = """!anki
front: O que é Docker?
back: Uma plataforma de containers baseada em cgroups e namespaces.
deck: Programming::Docker
tags: docker, containers, devops
type: Basic
"""
        payload = self.parser.parse_message(raw)
        self.assertEqual(payload.front, "O que é Docker?")
        self.assertEqual(payload.back, "Uma plataforma de containers baseada em cgroups e namespaces.")
        self.assertEqual(payload.deck, "Programming::Docker")
        self.assertEqual(payload.tags, ["docker", "containers", "devops"])
        self.assertEqual(payload.note_type, "Basic")

    def test_parse_multiline_and_code_blocks(self):
        raw = """!anki
front: Como criar uma função lambda em Python?
back: Sintaxe:
```python
square = lambda x: x ** 2
print(square(4)) # 16
```
tags: #python #lambdas
"""
        payload = self.parser.parse_message(raw)
        self.assertEqual(payload.front, "Como criar uma função lambda em Python?")
        self.assertIn("```python", payload.back)
        self.assertIn("square = lambda x: x ** 2", payload.back)
        self.assertEqual(payload.tags, ["python", "lambdas"])

    def test_cloze_auto_detection(self):
        raw = """!anki
front: O {{c1::TCP}} provê confiabilidade, enquanto o {{c2::UDP}} foca em velocidade.
deck: Redes
tags: networking, tcp
"""
        payload = self.parser.parse_message(raw)
        self.assertEqual(payload.note_type, "Cloze")
        self.assertEqual(payload.deck, "Redes")
        self.assertIn("{{c1::TCP}}", payload.front)

    def test_missing_front_raises_error(self):
        raw = """!anki
back: Resposta sem pergunta.
deck: Default
"""
        with self.assertRaises(ParserError):
            self.parser.parse_message(raw)

    def test_tag_normalization(self):
        tags1 = self.parser._parse_tags("python, docker; devops #linux infra")
        self.assertEqual(tags1, ["python", "docker", "devops", "linux", "infra"])

    def test_event_metadata_propagation(self):
        event = DiscordMessageEvent(
            id="msg_998877",
            content="!anki\nfront: Q\nback: A",
            author=DiscordUser(id="usr_123", name="Alice"),
            channel=DiscordChannel(id="chn_456", guild_id="gld_789"),
        )
        payload = self.parser.parse_message(event.content, event)
        self.assertEqual(payload.message_id, "msg_998877")
        self.assertEqual(payload.author_id, "usr_123")
        self.assertEqual(payload.author_name, "Alice")
        self.assertEqual(payload.channel_id, "chn_456")
        self.assertEqual(payload.guild_id, "gld_789")


if __name__ == "__main__":
    unittest.main()
