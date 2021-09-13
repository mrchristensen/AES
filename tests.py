import unittest
from unittest import TestCase

from main import xtime, ff_mult, sub_word, rot_word


class TestAES(unittest.TestCase):
    pass


class TestFiniteFieldArithmetic(TestAES):
    def test_xtime_no_mod(self):
        self.assertEqual(xtime(0x57), 0xae)

    def test_xtime_yes_mod(self):
        self.assertEqual(xtime(0xae), 0x47)

    def test_xtime_from_spec(self):
        self.assertEqual(xtime(0x57), 0xae)
        self.assertEqual(xtime(0xae), 0x47)
        self.assertEqual(xtime(0x47), 0x8e)
        self.assertEqual(xtime(0x8e), 0x07)

    def test_ff_mult(self):
        self.assertEqual(ff_mult(0x57, 0x13), 0xfe)  # from spec


class TestKeyExpansion(TestAES):
    def test_sub_word(self):
        self.assertEqual(sub_word(0x00102030), 0x63cab704)
        self.assertEqual(sub_word(0x40506070), 0x0953d051)
        self.assertEqual(sub_word(0x8090a0b0), 0xcd60e0e7)
        self.assertEqual(sub_word(0xc0d0e0f0), 0xba70e18c)

    def test_rot_word(self):
        self.assertEqual(rot_word(0x09cf4f3c), 0xcf4f3c09)
        self.assertEqual(rot_word(0x2a6c7605), 0x6c76052a)
        self.assertEqual(rot_word(0x00ff0000), 0xff000000)
        self.assertEqual(rot_word(0xff000000), 0x000000ff)
