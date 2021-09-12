import unittest
from unittest import TestCase

from main import xtime, ff_mult


class TestAES(unittest.TestCase):
    pass


class Test_xtime(TestAES):
    def test_xtime_no_mod(self):
        self.assertEqual(xtime(0x57), 0xae)

    def test_xtime_yes_mod(self):
        self.assertEqual(xtime(0xae), 0x47)

    def test_xtime_from_spec(self):
        self.assertEqual(xtime(0x57), 0xae)
        self.assertEqual(xtime(0xae), 0x47)
        self.assertEqual(xtime(0x47), 0x8e)
        self.assertEqual(xtime(0x8e), 0x07)


class Test_ff_mult(TestCase):
    def test_ff_mult(self):
        self.assertEqual(ff_mult(0x57, 0x13), 0xfe)  # from spec
