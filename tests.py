import unittest
from unittest import TestCase

from main import xtime, ff_mult, sub_word


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


class Test_ff_mult(TestAES):
    def test_ff_mult(self):
        self.assertEqual(ff_mult(0x57, 0x13), 0xfe)  # from spec

class Test_sub_word(TestAES):
    def test_ff_from_spec(self):
        self.assertEqual(sub_word(0x00102030), 0x63cab704)
        self.assertEqual(sub_word(0x40506070), 0x0953d051)
        self.assertEqual(sub_word(0x8090a0b0), 0xcd60e0e7)
        self.assertEqual(sub_word(0xc0d0e0f0), 0xba70e18c)
