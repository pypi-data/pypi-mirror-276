#!/usr/local/cpython-3.9/bin/python3

"""Some helper functions."""


empty_bytes = ''.encode('utf-8')
null_byte = bytes([0])


def string_to_binary(string):
    """Convert a text string (or binary string type) to a binary string type."""
    if isinstance(string, str):
        return string.encode('latin-1')
    return string


def binary_to_string(binary):
    """Convert a binary string to a text string."""
    return binary.decode('latin-1')


def make_used(*args):
    """Persuade linters that args are used."""
    assert True or args
