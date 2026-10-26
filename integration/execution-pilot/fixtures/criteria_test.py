"""Coordinator-only independent behavior oracle; not a candidate input."""
import sys
import unittest

sys.path.insert(0, sys.argv.pop(1))
from streamer import Stream


class CancellationContract(unittest.TestCase):
    def test_cancel_pending_delivery(self):
        stream = Stream(["first", "late"])
        self.assertEqual(next(stream), "first")
        stream.cancel()
        self.assertEqual(list(stream), [], "cancel delivered a late chunk")
        self.assertFalse(stream.active)
        self.assertTrue(stream.cancelled)

    def test_cancel_before_start_and_idempotent(self):
        stream = Stream(["late"])
        stream.cancel()
        stream.cancel()
        self.assertEqual(list(stream), [])
        self.assertFalse(stream.active)

    def test_normal_exhaustion(self):
        stream = Stream(["a", "b"])
        self.assertEqual(list(stream), ["a", "b"])
        self.assertFalse(stream.active)
        self.assertFalse(stream.cancelled)


if __name__ == "__main__":
    unittest.main(verbosity=2)
