#!/usr/bin/env python

"""
base255 strings.

You can think of them as a string representation of a number (serialized), and also as a null-terminatable number without any
practical limit on how large a number it can store
"""

# The representation with these "base255" strings, is:
#         A series of values, from 1 to 255, which when multiplied suitably, yield the original number.
#         The base255 representation will never contain a null (except optionally at the end), which means that you can
#         separate them with nulls in a string
#         The least significant 1..255 will always be the first character of the string


# The encoding overhead should be pretty low, since we're really only dropping 1 value per byte

# Note that this cannot represent numbers < 0.   0 is represented as a control-A.  But non-negative integers should be fine.

import sys

null_byte = bytes([0])


def number_to_base255(number):
    """Convert a number to a base255 string."""
    # least significant "byte" will be first in result
    byte255_list = []
    # take it apart as a series of numbers
    while number != 0:
        byte255_list.append((number % 255) + 1)
        number = number // 255
    if byte255_list == []:
        byte255_list.append(0 + 1)
    byte255_list.reverse()
    return bytes(byte255_list)


def base255_to_number(base255):
    """Convert a base255 string back to a number."""
    if base255[-1:] == null_byte:
        temp = base255[:-1]
    else:
        temp = base255
    if null_byte in temp:
        sys.stderr.write('Misplaced null in base255\n')
    # least signficant "byte" is first in base255
    list_ = temp
    list_minus_1 = [x - 1 for x in list_]
    number = 0
    for byte255 in list_minus_1:
        number = number * 255 + byte255
    return number
