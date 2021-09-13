import unittest
import numpy as np

from main import xtime, ff_mult, sub_word, rot_word, key_expansion, sub_bytes, shift_rows, mix_columns, add_round_key


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

    def test_256_key_expansion(self):  # from spec
        key = np.array([0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe,
                        0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81,
                        0x1f, 0x35, 0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7,
                        0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4])

        expected_result = np.array([
            0x603deb10, 0x15ca71be, 0x2b73aef0, 0x857d7781,
            0x1f352c07, 0x3b6108d7, 0x2d9810a3, 0x0914dff4,
            0x9ba35411, 0x8e6925af, 0xa51a8b5f, 0x2067fcde,
            0xa8b09c1a, 0x93d194cd, 0xbe49846e, 0xb75d5b9a,
            0xd59aecb8, 0x5bf3c917, 0xfee94248, 0xde8ebe96,
            0xb5a9328a, 0x2678a647, 0x98312229, 0x2f6c79b3,
            0x812c81ad, 0xdadf48ba, 0x24360af2, 0xfab8b464,
            0x98c5bfc9, 0xbebd198e, 0x268c3ba7, 0x09e04214,
            0x68007bac, 0xb2df3316, 0x96e939e4, 0x6c518d80,
            0xc814e204, 0x76a9fb8a, 0x5025c02d, 0x59c58239,
            0xde136967, 0x6ccc5a71, 0xfa256395, 0x9674ee15,
            0x5886ca5d, 0x2e2f31d7, 0x7e0af1fa, 0x27cf73c3,
            0x749c47ab, 0x18501dda, 0xe2757e4f, 0x7401905a,
            0xcafaaae3, 0xe4d59b34, 0x9adf6ace, 0xbd10190d,
            0xfe4890d1, 0xe6188d0b, 0x046df344, 0x706c631e])

        result = key_expansion(key, 256)

        self.assertTrue(np.array_equal(result, expected_result))


class TestCipher(TestAES):
    def test_sub_bytes(self):
        np.set_printoptions(formatter={'int': hex})
        state = np.array([[0x19, 0xa0, 0x9a, 0xe9],
                          [0x3d, 0xf4, 0xc6, 0xf8],
                          [0xe3, 0xe2, 0x8d, 0x48],
                          [0xbe, 0x2b, 0x2a, 0x08]], dtype=np.uint8)

        sub_expected_result = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                                        [0x27, 0xbf, 0xb4, 0x41],
                                        [0x11, 0x98, 0x5d, 0x52],
                                        [0xae, 0xf1, 0xe5, 0x30]], dtype=np.uint8)

        sub_result = sub_bytes(state)

        self.assertTrue(np.array_equal(sub_result, sub_expected_result))

    def test_shift_rows(self):
        np.set_printoptions(formatter={'int': hex})
        state = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                          [0x27, 0xbf, 0xb4, 0x41],
                          [0x11, 0x98, 0x5d, 0x52],
                          [0xae, 0xf1, 0xe5, 0x30]], dtype=np.uint8)

        shift_expected_result = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                                          [0xbf, 0xb4, 0x41, 0x27],
                                          [0x5d, 0x52, 0x11, 0x98],
                                          [0x30, 0xae, 0xf1, 0xe5]], dtype=np.uint8)

        shift_result = shift_rows(state)

        print("expected state:\n", shift_expected_result)

        self.assertTrue(np.array_equal(shift_result, shift_expected_result))

    def test_mix_columns_1(self):
        np.set_printoptions(formatter={'int': hex})
        state = np.array([[0xd4, 0xe0, 0xb8, 0x1e],
                          [0xbf, 0xb4, 0x41, 0x27],
                          [0x5d, 0x52, 0x11, 0x98],
                          [0x30, 0xae, 0xf1, 0xe5]], dtype=np.uint8)

        mix_expected_result = np.array([[0x04, 0xe0, 0x48, 0x28],
                                        [0x66, 0xcb, 0xf8, 0x06],
                                        [0x81, 0x19, 0xd3, 0x26],
                                        [0xe5, 0x9a, 0x7a, 0x4c]], dtype=np.uint8)

        mix_result = mix_columns(state)

        self.assertTrue(np.array_equal(mix_result, mix_expected_result))

    def test_mix_columns_2(self):
        np.set_printoptions(formatter={'int': hex})
        state = np.array([[0x49, 0x45, 0x7f, 0x77],
                          [0xdb, 0x39, 0x02, 0xde],
                          [0x87, 0x53, 0xd2, 0x96],
                          [0x3b, 0x89, 0xf1, 0x1a]], dtype=np.uint8)

        mix_expected_result = np.array([[0x58, 0x1b, 0xdb, 0x1b],
                                        [0x4d, 0x4b, 0xe7, 0x6b],
                                        [0xca, 0x5a, 0xca, 0xb0],
                                        [0xf1, 0xac, 0xa8, 0xe5]], dtype=np.uint8)

        mix_result = mix_columns(state)

        self.assertTrue(np.array_equal(mix_result, mix_expected_result))

    def test_add_round_key(self):
        np.set_printoptions(formatter={'int': hex})
        state = np.array([[0x04, 0xe0, 0x48, 0x28],
                          [0x66, 0xcb, 0xf8, 0x06],
                          [0x81, 0x19, 0xd3, 0x26],
                          [0xe5, 0x9a, 0x7a, 0x4c]], dtype=np.uint8)

        round_expected_result = np.array([[0xa4, 0x68, 0x6b, 0x02],
                                          [0x9c, 0x9f, 0x5b, 0x6a],
                                          [0x7f, 0x35, 0xea, 0x50],
                                          [0xf2, 0x2b, 0x43, 0x49]], dtype=np.uint8)

        round_result = add_round_key(state,w,4)

        self.assertTrue(np.array_equal(round_result, round_expected_result))