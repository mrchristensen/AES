import numpy as np
import sys

# Rcon[] is 1-based, so the first entry is just a place holder
Rcon = np.array([
    0x00000000,
    0x01000000, 0x02000000, 0x04000000, 0x08000000,
    0x10000000, 0x20000000, 0x40000000, 0x80000000,
    0x1B000000, 0x36000000, 0x6C000000, 0xD8000000,
    0xAB000000, 0x4D000000, 0x9A000000, 0x2F000000,
    0x5E000000, 0xBC000000, 0x63000000, 0xC6000000,
    0x97000000, 0x35000000, 0x6A000000, 0xD4000000,
    0xB3000000, 0x7D000000, 0xFA000000, 0xEF000000,
    0xC5000000, 0x91000000, 0x39000000, 0x72000000,
    0xE4000000, 0xD3000000, 0xBD000000, 0x61000000,
    0xC2000000, 0x9F000000, 0x25000000, 0x4A000000,
    0x94000000, 0x33000000, 0x66000000, 0xCC000000,
    0x83000000, 0x1D000000, 0x3A000000, 0x74000000,
    0xE8000000, 0xCB000000, 0x8D000000
])

Sbox = np.array([
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
])

InvSbox = np.array([
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
])


def get_Nk(AES_type):
    if AES_type == 128:
        return 4
    elif AES_type == 192:
        return 6
    elif AES_type == 256:
        return 8
    else:
        return None


def get_Nb(AES_type):
    if AES_type == 128 or AES_type == 192 or AES_type == 256:
        return 4
    else:
        return None


def get_Nr(AES_type):
    if AES_type == 128:
        return 10
    elif AES_type == 192:
        return 12
    elif AES_type == 256:
        return 14
    else:
        return None


def ff_mult(num1, num2):  # Num 1 will always be bigger
    # print("ff_mult() start")
    res = 0
    table = []
    mask = 0x01

    for i in range(0, 8):
        # print(i)

        if i == 0:
            table.append(num1)
            # print(hex(num1))
        else:
            table.append(xtime(table[i - 1]))
            # print(hex(xtime(table[i - 1])))

        if num2 & mask != 0:
            # print("xor the thing")
            # print(hex(table[i]))
            res = res ^ table[i]
        mask = mask << 1

    # print(table)
    # print("table:\n")
    # print('\n'.join([hex(i) for i in table]))

    # print("ff_mult() end")
    return res


def xtime(num):
    # print("xtime() start")
    bit_lost = False
    if num & 0x80 != 0:
        bit_lost = True

    num = num << 1

    if bit_lost:
        num = num ^ 0x11b

    # print("xtime() end")
    return num


def sub_word(four_byte_word):
    mask = 0x0f
    ret = 0x00
    # print("word: " + hex(four_byte_word))

    for index in range(4):
        # print("index: ", index)

        # print("mask: ", hex(mask))
        j = (four_byte_word & mask) >> (2 * index) * 4
        mask = mask << 4
        # print("mask: ", hex(mask))
        i = (four_byte_word & mask) >> (2 * index) * 4 + 4
        mask = mask << 4

        # print("i,j", hex(i), hex(j))

        byte_to_add = Sbox[i, j]
        # print("byte to add: ", hex(byte_to_add))

        byte_to_add_shifted = int(byte_to_add << (index * 8))

        if byte_to_add_shifted < 0:  # Fixed the stupid signed bug if the first bit is on: https://stackoverflow.com/questions/20766813/how-to-convert-signed-to-unsigned-integer-in-python
            byte_to_add_shifted += 1 << 32

        # print("to add to ret: ", hex(byte_to_add_shifted))

        ret = ret | byte_to_add_shifted
        # print("ret so far: ", hex(ret))

    # print("final ret: ", hex(ret))
    return ret


def rot_word(four_byte_word):
    res = 0x00
    mask = 0xff000000
    # print("original word: ", hex(four_byte_word))

    byte = four_byte_word & mask
    # print("byte: ", hex(byte))

    byte_shifted = byte >> 24
    # print("byte shifted: ", hex(byte_shifted))

    res = res | byte_shifted
    # print("res: ", hex(res))

    for index in range(3):
        mask = mask >> 8

        # print("index: ", index)
        # print("mask: ", hex(mask))

        byte = (four_byte_word & mask)
        # print("byte: ", hex(byte))

        byte_shifted = byte << 8
        # print("byte shifted: ", hex(byte_shifted))

        res = res | byte_shifted
        # print("res so far: ", hex(res))

    return res


def key_expansion(key,
                  AES_type):  # Nk = Number of 32-bit words comprising the Cipher Key. (Nk = 4, 6, or 8) (Also see Sec. 6.3.)
    Nb = get_Nb(AES_type)
    Nr = get_Nr(AES_type)
    Nk = get_Nk(AES_type)

    word = np.zeros(shape=Nb * (Nr + 1), dtype=np.uint)
    # print("empty word: ", word.astype(int))
    temp = np.empty(shape=Nb * (Nr + 1))

    i = 0

    while i < Nk:
        # print("\ni: ", i)
        next_word = int.from_bytes(bytearray([key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]]), "big")
        # print("Next word: ", np.array([key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]]))
        # print("Next word converted: ", hex(next_word))

        word[i] = next_word
        # print(word.astype(int))
        i = i + 1

        if next_word & 0x80000000 > 0:
            # print("got em")
            word[i] = word[i] + 1 << 32  # todo: turn this into a function
            # print("new word:\n", word)

    # print("\n\nFinished initial loop\n")

    i = Nk

    while i < Nb * (Nr + 1):
        temp = word[i - 1]
        # print("temp:\n", temp)
        if i % Nk == 0:
            temp = sub_word(rot_word(temp)) ^ Rcon[int(i / Nk)]
        elif Nk > 6 and i % Nk == 4:
            temp = sub_word(temp)
        word[i] = word[i - Nk] ^ temp
        i = i + 1

    # print("final word:\n", word)
    return word


def sub_bytes(state):
    # print("og state:\n", state)
    with np.nditer(state, op_flags=['readwrite']) as it:
        for byte in it:
            # print("byte: ", hex(byte))
            i = (byte & 0xf0) >> 4
            j = byte & 0x0f
            # print("i, j: ", hex(i), hex(j))
            byte[...] = Sbox[i, j]
            # print("new byte: ", hex(byte))
            # print("new state:\n", state)
    return state


def inv_sub_bytes(state):
    # print("og state:\n", state)
    with np.nditer(state, op_flags=['readwrite']) as it:
        for byte in it:
            # print("byte: ", hex(byte))
            i = (byte & 0xf0) >> 4
            j = byte & 0x0f
            # print("i, j: ", hex(i), hex(j))
            byte[...] = InvSbox[i, j]
            # print("new byte: ", hex(byte))
            # print("new state:\n", state)
    return state


def shift_rows(state):
    # print("og state:\n", state)
    for i in range(4):
        # print("i: ", i)
        state[i] = np.roll(state[i], 4 - i)
        # print("new state:\n", state)

    return state


def inv_shift_rows(state):
    # print("og state:\n", state)
    for i in range(4):
        # print("i: ", i)
        state[i] = np.roll(state[i], i)
        # print("new state:\n", state)

    return state


def mix_columns(state):
    # print("og state:\n", state)
    state_copy = np.copy(state)
    for c in range(4):
        # print("\ncol: ", c)
        state[0, c] = ff_mult(state_copy[0, c], 0x02) ^ ff_mult(state_copy[1, c], 0x03) ^ state_copy[2, c] ^ state_copy[
            3, c]
        state[1, c] = state_copy[0, c] ^ ff_mult(state_copy[1, c], 0x02) ^ ff_mult(state_copy[2, c], 0x03) ^ state_copy[
            3, c]
        state[2, c] = state_copy[0, c] ^ state_copy[1, c] ^ ff_mult(state_copy[2, c], 0x02) ^ ff_mult(state_copy[3, c],
                                                                                                      0x03)
        state[3, c] = ff_mult(state_copy[0, c], 0x03) ^ state_copy[1, c] ^ state_copy[2, c] ^ ff_mult(state_copy[3, c],
                                                                                                      0x02)
        # print("new state:\n", state)

    # print("final state:\n", state)
    return state


def inv_mix_columns(state):
    # print("og state:\n", state)
    state_copy = np.copy(state)
    for c in range(4):
        # print("\ncol: ", c)
        state[0, c] = ff_mult(state_copy[0, c], 0x0e) ^ ff_mult(state_copy[1, c], 0x0b) ^ ff_mult(state_copy[2, c], 0x0d) ^ ff_mult(state_copy[3, c], 0x09)
        state[1, c] = ff_mult(state_copy[0, c], 0x09) ^ ff_mult(state_copy[1, c], 0x0e) ^ ff_mult(state_copy[2, c], 0x0b) ^ ff_mult(state_copy[3, c], 0x0d)
        state[2, c] = ff_mult(state_copy[0, c], 0x0d) ^ ff_mult(state_copy[1, c], 0x09) ^ ff_mult(state_copy[2, c], 0x0e) ^ ff_mult(state_copy[3, c], 0x0b)
        state[3, c] = ff_mult(state_copy[0, c], 0x0b) ^ ff_mult(state_copy[1, c], 0x0d) ^ ff_mult(state_copy[2, c], 0x09) ^ ff_mult(state_copy[3, c], 0x0e)
        # print("new state:\n", state)

    # print("final state:\n", state)
    return state


def add_round_key(state, w):
    # return np.bitwise_or(state, w)
    new_state = np.array([[0x00, 0x00, 0x00, 0x00],
                          [0x00, 0x00, 0x00, 0x00],
                          [0x00, 0x00, 0x00, 0x00],
                          [0x00, 0x00, 0x00, 0x00]], dtype=np.uint8)

    for col in range(4):
        for row in range(4):
            new_state[col, row] = state[col, row] ^ w[col, row]

    return new_state


def create_byte_matrix(array):
    byte_matrix = np.array([[0x00, 0x00, 0x00, 0x00],
                            [0x00, 0x00, 0x00, 0x00],
                            [0x00, 0x00, 0x00, 0x00],
                            [0x00, 0x00, 0x00, 0x00]], dtype=np.uint8)
    i, j = 0, 0

    for row in array:
        # print("row: ", hex(row))
        byte_matrix[i, j] = (row & 0xff000000) >> 3 * 8
        i += 1
        byte_matrix[i, j] = (row & 0x00ff0000) >> 2 * 8
        i += 1
        byte_matrix[i, j] = (row & 0x0000ff00) >> 1 * 8
        i += 1
        byte_matrix[i, j] = (row & 0x000000ff)

        j += 1
        i = 0
        # print("byte_matrix so far:\n", byte_matrix)

    return byte_matrix


def cipher(input, key, type):
    Nb = get_Nb(type)
    Nr = get_Nr(type)

    print("round[ 0 ].input\t", format_input(input))
    print("round[ 0 ].k_sch\t", format_input(key))
    state = input.reshape(4, 4).T
    # print("state:\n", state)
    # print("key:\n", key)
    w = key_expansion(key, type)
    # print("w:\n", w)

    # print(create_byte_matrix(w[0:4]))

    state = add_round_key(state, create_byte_matrix(w[0:Nb]))  # See Sec. 5.1.4

    for round in range(1, Nr):  # for round = 1 step 1 to Nr–1: #todo: make sure range is good
        print("round[", round, "].start\t", format_output(state))

        state = sub_bytes(state)  # See Sec. 5.1.1
        print("round[", round, "].s_box\t", format_output(state))
        # print("\nafter sub_bytes:\n", state)
        state = shift_rows(state)  # See Sec. 5.1.2
        print("round[", round, "].s_row\t", format_output(state))
        # print("\nafter shift_rows:\n", state)
        state = mix_columns(state)  # See Sec. 5.1.3
        print("round[", round, "].m_col\t", format_output(state))
        # print("\nafter mix_columns:\n", state)
        state = add_round_key(state, create_byte_matrix(w[round * Nb:(round + 1) * Nb]))
        print("round[", round, "].k_sch\t", format_output(create_byte_matrix(w[round * Nb:(round + 1) * Nb])))
        # print("round Key value:\n", create_byte_matrix(w[round * Nb:(round + 1) * Nb]))

    print("round[ 10].start\t", format_output(state))

    # print("start of round:\n", state)
    state = sub_bytes(state)
    print("round[ 10].s_box\t", format_output(state))
    # print("\nafter sub_bytes:\n", state)
    state = shift_rows(state)
    print("round[ 10].s_row\t", format_output(state))
    # print("\nafter shift_rows:\n", state)
    # print("round Key value:\n", create_byte_matrix(w[Nr * Nb:(Nr + 1) * Nb]))
    state = add_round_key(state, create_byte_matrix(w[Nr * Nb:(Nr + 1) * Nb]))
    print("round[ 10].k_sch\t", format_output(create_byte_matrix(w[Nr * Nb:(Nr + 1) * Nb])))

    print("round[ 10].output\t", format_output(state))
    # print("output:\n", state)

    return state


def inv_cipher(input, key, type):
    Nb = get_Nb(type)
    Nr = get_Nr(type)

    print("round[ 0 ].iinput\t", format_input(input))
    print("round[ 0 ].ik_sch\t", format_input(key))
    # print("input:\n", input)
    state = input.reshape(4, 4).T
    # print("state:\n", state)
    # print("key:\n", key)
    w = key_expansion(key, type)
    # print("w:\n", w)

    state = add_round_key(state, create_byte_matrix(w[Nr * Nb:(Nr + 1) * Nb]))  # See Sec. 5.1.4

    for round in reversed(range(1, Nr)):  # for round = 1 step 1 to Nr–1
        print("round[", 10 - round, "].istart\t", format_output(state))

        # print("\nround:\n", round)
        # print("start of round:\n", state)

        state = inv_shift_rows(state)  # See Sec. 5.1.2
        print("round[", 10 - round, "].is_row\t", format_output(state))
        # print("\nafter inv_shift_rows:\n", state)
        state = inv_sub_bytes(state)  # See Sec. 5.1.1
        print("round[", 10 - round, "].is_box\t", format_output(state))
        # print("\nafter inv_sub_bytes:\n", state)
        state = add_round_key(state, create_byte_matrix(w[round * Nb:(round + 1) * Nb]))
        print("round[", 10 - round, "].ik_sch\t", format_output(create_byte_matrix(w[round * Nb:(round + 1) * Nb])))
        print("round[", 10 - round, "].ik_add\t", format_output(state))
        # print("round Key value:\n", create_byte_matrix(w[round * Nb:(round + 1) * Nb]))
        state = inv_mix_columns(state)  # See Sec. 5.1.3
        print("round[", 10 - round, "].im_col\t", format_output(state))
        # print("\nafter inv_mix_columns:\n", state)

    print("round[ 10].istart\t", format_output(state))
    # print("\nround: 10 (special round)\n")
    # print("start of round:\n", state)

    state = inv_shift_rows(state)
    print("round[ 10].is_row\t", format_output(state))
    # print("\nafter inv_shift_rows:\n", state)
    state = inv_sub_bytes(state)
    print("round[ 10].is_box\t", format_output(state))
    # print("\nafter inv_sub_bytes:\n", state)
    # print("round Key value:\n", create_byte_matrix(w[0:Nb]))
    state = add_round_key(state, create_byte_matrix(w[0:Nb]))
    print("round[ 10].ik_sch\t", format_output(create_byte_matrix(w[0:Nb])))

    print("round[ 10].ioutput\t", format_output(state))
    # print("output:\n", state)

    return state


def parse_input_string(input_string):
    return np.array([int(input_string[i:i + 2], base=16) for i in range(0, len(input_string), 2)])


def format_output(array):
    # print("array:\n", array)

    return_string = ""

    array = array.T

    for row in array:
        # print("row: ", row)
        for entry in row:
            # print("entry: ", hex(entry))
            # print("str(hex(entry))[2:5]: ", str(hex(entry))[2:5])
            # return_string += str(hex(entry))[2:5]
            # print("thing: ", "{:02x}".format(entry))
            return_string += "{:02x}".format(entry)
            # print("return_string so far: ", return_string)

    return return_string


def format_input(array):
    # print("array:\n", array)

    return_string = ""

    array = array.T

    for entry in array:
        # print("entry: ", hex(entry))
        # print("str(hex(entry))[2:5]: ", str(hex(entry))[2:5])
        # return_string += str(hex(entry))[2:5]
        # print("thing: ", "{:02x}".format(entry))
        return_string += "{:02x}".format(entry)
        # print("return_string so far: ", return_string)

    return return_string


def encrypt():
    print("Let's do encryption:\n")
    aes_type = None
    while aes_type != 128 and aes_type != 192 and aes_type != 256:
        aes_type = int(input("Input AES type (128, 192, or 256): "))

    key_input = input("Input the key: ")

    plain_text = input("Input the message: ")

    parsed_plain_text = parse_input_string(plain_text)
    # print("parsed_plain_text:\n", parsed_plain_text)
    parsed_key = parse_input_string(key_input)
    # print("parsed_key:\n", parsed_key)

    output = cipher(parsed_plain_text, parsed_key, aes_type)
    # print("output (un=formatted): ", output)

    formatted_output = format_output(output)
    # print("output (formatted): ", formatted_output)


def decrypt():
    print("Let's do decryption:\n")
    aes_type = None
    while aes_type != 128 and aes_type != 192 and aes_type != 256:
        aes_type = int(input("Input AES type (128, 192, or 256): "))

    key_input = input("Input the key: ")

    encrypted_text = input("Input the message: ")

    parsed_encrypted_text = parse_input_string(encrypted_text)
    # print("parsed_encrypted_text:\n", parsed_encrypted_text)
    parsed_key = parse_input_string(key_input)
    # print("parsed_key:\n", parsed_key)

    output = inv_cipher(parsed_encrypted_text, parsed_key, aes_type)
    # print("output (un=formatted): ", output)

    formatted_output = format_output(output)
    # print("output (formatted): ", formatted_output)


if __name__ == '__main__':
    # np.set_printoptions(formatter={'int': hex})

    while True:
        mode = input("Input the mode (encrypt or decrypt): ")

        if mode == "encrypt":
            encrypt()
        elif mode == "decrypt":
            decrypt()
        elif mode == "exit":
            exit()
