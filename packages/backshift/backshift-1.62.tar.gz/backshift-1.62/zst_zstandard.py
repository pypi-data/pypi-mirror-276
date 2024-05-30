
"""Compress and decompress data using the zstd module."""

import zstandard

# Technically, we could just do this with a pair of assignment statements, instead of function wrappers.  But that could
# expose more of the underlying API than we want.


def compress(data):
    """Compress data using defaults."""
    return zstandard.compress(data)


def decompress(data):
    """Decompress data."""
    return zstandard.decompress(data)
