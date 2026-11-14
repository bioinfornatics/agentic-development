"""Public behavior contract: Stop cancels one active request exactly once."""
import unittest
from controller import Controller

class Transport:
    def __init__(self):
        self.calls = 0
    def cancel(self):
        self.calls += 1

class Cancellation(unittest.TestCase):
    def setUp(self):
        self.transport = Transport()
        self.controller = Controller(self.transport)
    def test_active_stop_once(self):
        self.controller.begin()
        self.controller.stop()
        self.controller.stop()
        self.assertEqual(self.transport.calls, 1)
        self.assertFalse(self.controller.active)
    def test_idle_stop(self):
        self.controller.stop()
        self.assertEqual(self.transport.calls, 0)
    def test_completed_stop(self):
        self.controller.begin()
        self.controller.complete()
        self.controller.stop()
        self.assertEqual(self.transport.calls, 0)

if __name__ == '__main__':
    unittest.main()
