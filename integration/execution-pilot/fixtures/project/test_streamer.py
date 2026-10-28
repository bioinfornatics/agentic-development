import unittest
from streamer import Stream


class SmokeTest(unittest.TestCase):
    def test_normal_stream(self):
        stream = Stream(["a", "b"])
        self.assertEqual(list(stream), ["a", "b"])
        self.assertFalse(stream.active)


if __name__ == "__main__":
    unittest.main()
