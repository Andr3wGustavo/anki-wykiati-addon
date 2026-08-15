"""
Unit tests for DiscordBridge and CommandRouter.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import config
from discord.bridge import DiscordBridge
from discord.commands import CommandRouter
from sync.queue import job_queue


class TestBridgeAndCommands(unittest.TestCase):
    def setUp(self):
        self.bridge = DiscordBridge()
        self.commands = CommandRouter()
        job_queue.clear()
        config.reset_to_defaults()

    def test_commands_help(self):
        reply = self.commands.handle_command("!anki-help")
        self.assertIsNotNone(reply)
        self.assertIn("Guia de Comandos", reply)
        self.assertIn("front:", reply)

    def test_commands_status(self):
        reply = self.commands.handle_command("!anki-status")
        self.assertIsNotNone(reply)
        self.assertIn("Status do Sistema", reply)

    def test_commands_ping(self):
        reply = self.commands.handle_command("!anki-ping")
        self.assertIsNotNone(reply)
        self.assertIn("Pong!", reply)

    def test_bridge_processes_valid_message(self):
        raw_msg = """!anki
front: O que é Kubernetes?
back: Um orquestrador de containers open source.
deck: DevOps::Kubernetes
tags: k8s, devops
"""
        success, reply = self.bridge.handle_incoming_message(raw_msg)
        self.assertTrue(success)
        self.assertIn("Card Enqueued", reply)
        self.assertIn("DevOps::Kubernetes", reply)
        self.assertEqual(job_queue.get_pending_count(), 1)

    def test_bridge_rejects_invalid_format(self):
        raw_msg = "!anki\nback: Only back without question"
        success, reply = self.bridge.handle_incoming_message(raw_msg)
        self.assertFalse(success)
        self.assertIn("Format Error", reply)


if __name__ == "__main__":
    unittest.main()
