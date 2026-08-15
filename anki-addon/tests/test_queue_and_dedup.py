"""
Unit tests for JobQueue and AntiDuplicationRegistry.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discord.models import CardPayload, JobStatus
from sync.dedup import AntiDuplicationRegistry
from sync.jobs import SyncJob
from sync.queue import JobQueue


class TestQueueAndDedup(unittest.TestCase):
    def setUp(self):
        self.queue = JobQueue(max_history=50)
        self.queue.clear()
        self.dedup = AntiDuplicationRegistry()
        self.dedup.clear()

    def test_queue_enqueue_and_fifo_order(self):
        p1 = CardPayload(front="Card 1", back="Ans 1")
        p2 = CardPayload(front="Card 2", back="Ans 2")

        j1 = self.queue.enqueue(p1)
        j2 = self.queue.enqueue(p2)

        self.assertEqual(self.queue.get_pending_count(), 2)

        next_job = self.queue.get_next()
        self.assertIsNotNone(next_job)
        self.assertEqual(next_job.id, j1.id)
        self.assertEqual(next_job.status, JobStatus.PROCESSING)

        self.queue.mark_success(next_job, note_id=1001)
        self.assertEqual(next_job.status, JobStatus.SUCCESS)

    def test_queue_retry_and_permanent_failure(self):
        p = CardPayload(front="Faulty Card", back="Ans")
        job = self.queue.enqueue(p)
        job.max_retries = 2

        # 1st attempt fails -> retry
        j1 = self.queue.get_next()
        self.queue.mark_failed(j1, "Connection timeout")
        self.assertEqual(j1.status, JobStatus.RETRY)
        self.assertEqual(self.queue.get_pending_count(), 1)

        # 2nd attempt fails -> permanent failure
        j2 = self.queue.get_next()
        self.queue.mark_failed(j2, "Database locked")
        self.assertEqual(j2.status, JobStatus.FAILED)
        self.assertEqual(self.queue.get_pending_count(), 0)

    def test_anti_duplication_fingerprint(self):
        p1 = CardPayload(front="What is RAM?", back="Random Access Memory", deck="CS")
        p2 = CardPayload(front="  what is ram?  ", back="random access memory", deck="CS")

        # Same semantic content -> same hash
        self.assertEqual(p1.compute_hash(), p2.compute_hash())

        # Register card
        self.assertFalse(self.dedup.is_duplicate("msg_101", p1.compute_hash()))
        self.dedup.register_processed("msg_101", p1.compute_hash(), note_id=500)

        # Now detected as duplicate by message ID
        self.assertTrue(self.dedup.is_duplicate("msg_101", "another_hash"))

        # And detected as duplicate by content hash
        self.assertTrue(self.dedup.is_duplicate("new_msg_id", p2.compute_hash()))


if __name__ == "__main__":
    unittest.main()
