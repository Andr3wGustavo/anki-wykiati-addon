"""
Unit tests for Smart Deck Routing.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import config
from discord.models import CardPayload
from routing.router import DeckRouter


class TestDeckRouter(unittest.TestCase):
    def setUp(self):
        self.router = DeckRouter()
        config.reset_to_defaults()
        config.set("routing.rules", [
            {"type": "tag", "pattern": "python", "deck": "Programming::Python"},
            {"type": "tag", "pattern": "docker", "deck": "DevOps::Docker"},
            {"type": "keyword", "pattern": "kubernetes", "deck": "DevOps::K8s"},
        ], save=False)

    def test_explicit_deck_priority(self):
        payload = CardPayload(
            front="Perguntas de Python",
            back="Respostas",
            deck="Custom::OverrideDeck",
            tags=["python"],
        )
        resolved = self.router.resolve_deck(payload)
        self.assertEqual(resolved, "Custom::OverrideDeck")

    def test_tag_rule_match(self):
        payload = CardPayload(
            front="O que é GIL?",
            back="Global Interpreter Lock",
            deck="Default",
            tags=["python", "interview"],
        )
        resolved = self.router.resolve_deck(payload)
        self.assertEqual(resolved, "Programming::Python")

    def test_keyword_rule_match(self):
        payload = CardPayload(
            front="O que é um Pod no Kubernetes?",
            back="Menor unidade de deploy",
            deck="Default",
            tags=["cloud"],
        )
        resolved = self.router.resolve_deck(payload)
        self.assertEqual(resolved, "DevOps::K8s")

    def test_fallback_to_default_deck(self):
        payload = CardPayload(
            front="Capital do Brasil?",
            back="Brasília",
            deck="Default",
            tags=["geography"],
        )
        resolved = self.router.resolve_deck(payload)
        self.assertEqual(resolved, "Default")


if __name__ == "__main__":
    unittest.main()
