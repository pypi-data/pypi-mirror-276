
"""
Provides functions for escaping and unescaping strings.

It's not very space-efficient - it doubles the length of the string.
But it's pretty easy to read the quoted strings, and the code
is simple.
"""

import constants_mod
import helpers


def ordinal(char):
    """Convert a character to its ordinal value."""
    if isinstance(char, int):
        return char
    int_list = helpers.string_to_binary(char)
    assert len(int_list) == 1
    byte_value = int_list[0]
    assert 0 <= byte_value <= 255, "byte_value has a strange value: {}".format(byte_value)
    return byte_value


def character(number):
    """Convert a single number from 0 to 255 to bytes."""
    if 0 <= ordinal(number) <= 255:
        return bytes([ordinal(number)])
    else:
        raise ValueError('Value %d not between 0 and 255 inclusive' % number)


def hexadecimal(hex_digit):
    """Convert a number from 0 to 15 to hexadecimal."""
    if hex_digit >= 0 and hex_digit <= 15:
        return '0123456789abcdef'[hex_digit]
    else:
        raise ValueError('Value %d not between 0 and 15 inclusive' % hex_digit)


def escape(string):
    """Escape a string for saving in a text format."""
    # Note that it might be nice to have an encoding that's more human-readable, but getting urllib.request.quote past
    # pylint was proving more trouble than it was worth
    # sys.stderr.write('Escaping %s\n' % pathname)
    special_set = set(constants_mod.Constants.b_special)
    underscore = ordinal(constants_mod.Constants.b_underscore)
    list_ = []
    for one_char in string:
        char = ordinal(one_char)
        if ordinal(constants_mod.Constants.b_a) <= char <= ordinal(constants_mod.Constants.b_z):
            list_.append(char)
            list_.append(underscore)
        elif ordinal(constants_mod.Constants.b_A) <= char <= ordinal(constants_mod.Constants.b_Z):
            list_.append(char)
            list_.append(underscore)
        elif ordinal(constants_mod.Constants.b_0) <= char <= ordinal(constants_mod.Constants.b_9):
            list_.append(char)
            list_.append(underscore)
        elif char in special_set:
            list_.append(char)
            list_.append(underscore)
        else:
            high_nybble = hexadecimal(char // 16)
            low_nybble = hexadecimal(char & 15)
            list_.append(ordinal(high_nybble))
            list_.append(ordinal(low_nybble))

    return bytes(list_)


def unescape(quoted_string):
    """Unescape an escaped string when retrieving from a text format."""
    list_ = []
    assert len(quoted_string) % 2 == 0

    for position in range(0, len(quoted_string), 2):
        if quoted_string[position + 1:position + 2] == constants_mod.Constants.b_underscore:
            list_.append(quoted_string[position])
        else:
            one_byte = quoted_string[position:position + 2]
            number = int(one_byte, 16)
            list_.append(character(number))

    ordinal_list = [ordinal(ch) for ch in list_]

    return bytes(ordinal_list)
