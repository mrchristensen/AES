import unittest
import numpy as np

from main import xtime, ff_mult, sub_word, rot_word, key_expansion


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

    def test_128_key_expansion(self):  # from spec
        key = np.array([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
                        0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
        expected_result = np.array([
            0x2b7e1516, 0x28aed2a6, 0xabf71588, 0x09cf4f3c,
            0xa0fafe17, 0x88542cb1, 0x23a33939, 0x2a6c7605,
            0xf2c295f2, 0x7a96b943, 0x5935807a, 0x7359f67f,
            0x3d80477d, 0x4716fe3e, 0x1e237e44, 0x6d7a883b,
            0xef44a541, 0xa8525b7f, 0xb671253b, 0xdb0bad00,
            0xd4d1c6f8, 0x7c839d87, 0xcaf2b8bc, 0x11f915bc,
            0x6d88a37a, 0x110b3efd, 0xdbf98641, 0xca0093fd,
            0x4e54f70e, 0x5f5fc9f3, 0x84a64fb2, 0x4ea6dc4f,
            0xead27321, 0xb58dbad2, 0x312bf560, 0x7f8d292f,
            0xac7766f3, 0x19fadc21, 0x28d12941, 0x575c006e,
            0xd014f9a8, 0xc9ee2589, 0xe13f0cc8, 0xb6630ca6])

        result = key_expansion(key, 128)

        self.assertTrue(np.array_equal(result, expected_result))

    def test_192_key_expansion(self):  # from spec
        key = np.array([0x8e, 0x73, 0xb0, 0xf7, 0xda, 0x0e, 0x64, 0x52,
                        0xc8, 0x10, 0xf3, 0x2b, 0x80, 0x90, 0x79, 0xe5,
                        0x62, 0xf8, 0xea, 0xd2, 0x52, 0x2c, 0x6b, 0x7b])

        expected_result = np.array([
            0x8e73b0f7, 0xda0e6452, 0xc810f32b, 0x809079e5,
            0x62f8ead2, 0x522c6b7b, 0xfe0c91f7, 0x2402f5a5,
            0xec12068e, 0x6c827f6b, 0x0e7a95b9, 0x5c56fec2,
            0x4db7b4bd, 0x69b54118, 0x85a74796, 0xe92538fd,
            0xe75fad44, 0xbb095386, 0x485af057, 0x21efb14f,
            0xa448f6d9, 0x4d6dce24, 0xaa326360, 0x113b30e6,
            0xa25e7ed5, 0x83b1cf9a, 0x27f93943, 0x6a94f767,
            0xc0a69407, 0xd19da4e1, 0xec1786eb, 0x6fa64971,
            0x485f7032, 0x22cb8755, 0xe26d1352, 0x33f0b7b3,
            0x40beeb28, 0x2f18a259, 0x6747d26b, 0x458c553e,
            0xa7e1466c, 0x9411f1df, 0x821f750a, 0xad07d753,
            0xca400538, 0x8fcc5006, 0x282d166a, 0xbc3ce7b5,
            0xe98ba06f, 0x448c773c, 0x8ecc7204, 0x01002202])

        result = key_expansion(key, 192)

        self.assertTrue(np.array_equal(result, expected_result))
