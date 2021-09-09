# import numpy as np

def ff_mult(num1, num2):  # Num 1 will always be bigger
    print("ff_mult() start")
    res = 0
    table = []
    mask = 0x01

    for i in range(0, 8):
        print(i)

        if i == 0:
            table.append(num1)
            print(hex(num1))
        else:
            table.append(xtime(table[i - 1]))
            print(hex(xtime(table[i - 1])))

        if num2 & mask != 0:
            print("xor the thing")
            print(hex(table[i]))
            res = res ^ table[i]
        mask = mask << 1

    # print(table)
    print("table:\n")
    print('\n'.join([hex(i) for i in table]))

    print("ff_mult() end")
    return res


def xtime(num):
    print("xtime() start")
    bit_lost = False
    if num & 0x80 != 0:
        bit_lost = True

    num = num << 1

    if bit_lost:
        num = num ^ 0x11b

    print("xtime() end")
    return num


if __name__ == '__main__':
    # np.set_printoptions(formatter={'int': hex})
    print("ff_mult result: " + hex(ff_mult(0x57, 0x13)))
    # print(hex(xtime(0x70)))
