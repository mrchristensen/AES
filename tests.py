import unittest
from main import xtime


class TestAES(unittest.TestCase):
    pass


class Testxtime(TestAES):
    def test_xtime_no_mod(self):
        self.assertEqual(xtime(0x57), 0xae)

    def test_xtime_yes_mod(self):
        self.assertEqual(xtime(0xae), 0x47)

