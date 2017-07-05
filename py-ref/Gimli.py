#!/usr/bin/env python3
from typing import List

R = 24
S = 9

Sheet = List[int]
State = List[Sheet]

"""State are seen as  a 3 x 4 x 32 array """

shift_x = 2  # a
shift_y = 1  # b
shift_z = 3  # c
rot_x = R  # d
rot_y = S  # e
rot_z = 0  # f


def rot(x: int, n: int) -> int:
    """Bitwise rotation (to the left) of n bits considering the \
    string of bits is 32 bits long"""
    x %= 1 << 32
    n %= 32
    # if n == 0:
    # print(hex(x), "=>", hex((x >> (32 - n)) | (x << n) % (1 << 32)))
    return (x >> (32 - n)) | (x << n) % (1 << 32)


def non_lin_perm_96(sheet: Sheet, a: int, b: int, c: int, d: int, e: int, f: int) -> Sheet:
    """Apply the non linear permutation on the 96 sheet of the state"""

    x,y,z = sheet
    x,y,z = rot(x,d),rot(y,e),rot(z,f)
    x,y,z = (
      x ^ (z << 1) ^ ((y & z) << a),
      y ^ x ^ ((x | z) << b),
      z ^ y ^ ((x & y) << c)
    )
    sheet[0] = z % (1 << 32)
    sheet[1] = y % (1 << 32)
    sheet[2] = x % (1 << 32)
    return sheet


def small_swap(state: State) -> State:
    for j in range(1):
        state[0][j], state[1][j], state[2][j], state[3][j] \
            = state[1][j], state[0][j], state[3][j], state[2][j]
    return state


def big_swap(state: State) -> State:
    for j in range(1):
        state[0][j], state[1][j], state[2][j], state[3][j] \
            = state[2][j], state[3][j], state[0][j], state[1][j]
    return state


def print_to_hex(x):
    for i in range(3):
        print(hex(x[0][i])[2:].zfill(8), hex(x[1][i])[2:].zfill(8), hex(x[2][i])[2:].zfill(8),
              hex(x[3][i])[2:].zfill(8), "")
    print("----------------------")


def gimli(state: State) -> State:
    """ Number of rounds has still to be determined """
    for outer_rounds in range(6):

        """ Apply the inner diffusion (96 bits) on the sheet """
        for inner_rounds in range(4):

            """ Apply the 96 Non linear permutation on each sheet """
            for i_sheet in range(4):
                state[i_sheet] = non_lin_perm_96(state[i_sheet], shift_x, shift_y, shift_z, rot_x, rot_y, rot_z)

            if inner_rounds == 0:
                state = small_swap(state)
            if inner_rounds == 2:
                state = big_swap(state)
            if inner_rounds == 0:
                state[0][0] ^= 0x9e377900
                state[0][0] ^= 24 - (outer_rounds * 4 + inner_rounds)

    return state
