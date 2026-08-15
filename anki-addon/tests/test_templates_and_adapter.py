"""
Unit tests for TemplateManager, NoteAdapter, and Markdown Formatter.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from anki.notes import NoteAdapter, _format_markdown_to_anki_html
from discord.models import CardPayload
from templates.manager import TemplateManager


class TestTemplatesAndAdapter(unittest.TestCase):
    def setUp(self):
        self.templates = TemplateManager()
        self.adapter = NoteAdapter()

    def test_markdown_formatting_to_html(self):
        md = "**Bold** and *Italic* and `code`"
        html = _format_markdown_to_anki_html(md)
        self.assertIn("<b>Bold</b>", html)
        self.assertIn("<i>Italic</i>", html)
        self.assertIn("<code>code</code>", html)

    def test_code_block_formatting(self):
        md = "Exemplo:\n```python\nprint('Hello')\n```"
        html = _format_markdown_to_anki_html(md)
        self.assertIn("<pre><code>print('Hello')</code></pre>", html)

    def test_map_fields_basic_model(self):
        payload = CardPayload(front="Q", back="A", extra="Notes")
        model_dict = {"name": "Basic", "flds": [{"name": "Front"}, {"name": "Back"}]}
        mapped = self.templates.map_fields_to_model(payload, model_dict)
        self.assertEqual(mapped["Front"], "Q")
        self.assertEqual(mapped["Back"], "A")

    def test_map_fields_cloze_model(self):
        payload = CardPayload(front="{{c1::Tokyo}} is in Japan.", back="Capital", note_type="Cloze")
        model_dict = {"name": "Cloze", "flds": [{"name": "Text"}, {"name": "Extra"}]}
        mapped = self.templates.map_fields_to_model(payload, model_dict)
        self.assertEqual(mapped["Text"], "{{c1::Tokyo}} is in Japan.")
        self.assertEqual(mapped["Extra"], "Capital")

    def test_create_note_headless_simulation(self):
        payload = CardPayload(front="Pergunta de Teste", back="Resposta de Teste", deck="TestDeck")
        note_id = self.adapter.create_note_from_payload(payload)
        self.assertIsInstance(note_id, int)
        self.assertGreater(note_id, 0)


if __name__ == "__main__":
    unittest.main()
