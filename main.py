# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import numpy as np

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def ff_mult(num1, num2):  # Num 1 will always be bigger
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
            print("xor the thang")
            print(hex(table[i]))
            res = res ^ table[i]
        mask = mask << 1

    # print(table)
    print("table:\n")
    print('\n'.join([hex(i) for i in table]))

    return res


def xtime(num):
    bit_lost = False
    if num & 0x80 != 0:
        bit_lost = True

    num = num << 1

    if bit_lost:
        num = num ^ 0x11b

    return num


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # np.set_printoptions(formatter={'int': hex})
    print(hex(ff_mult(0x57, 0x13)))
    # print(hex(xtime(0x70)))
