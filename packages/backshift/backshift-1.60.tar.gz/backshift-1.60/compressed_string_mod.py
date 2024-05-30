#!/usr/bin/python

"""Provides functions for compressing and decompressing strings, all in memory."""

# 0: Unused
# 1: Not compressed
# 2: Compressed with pack: .z
# 3: Compressed with compress: .Z
# 4: Compressed with gzip: .gz
# 5: Compressed with bzip2: .bz2 (quite a bit slower than gzip, but packs harder)
# 6: Compressed with xz -2: .xz (quite a bit faster than bz2, only a tiny bit larger)
# 7: Compressed with xz -6: .xz (packs harder than bzip2, but slower)
# 8: Compressed with zstandard: .zst (gives a balance of compression ratio and performance. Laughably faster than xz)
#
# Brotli may prove worth adding:
# http://tech.slashdot.org/story/15/09/22/1723219/google-launches-brotli-a-new-open-source-compression-algorithm-for-the-web
#
# At this time, only 1, 5 and 7 are used

import sys

try:
    import bz2 as bz2_mod
except ImportError:
    HAVE_BZ2 = False
else:
    HAVE_BZ2 = True

import constants_mod
import helpers
import stringio
import xz_mod
import zst_mod


def compress_string(data, bz2_announced=False):
    """
    Compress a string.

    1) If we have zstandard, try to use it.
    2) Fallback: if we have bz2, try to use that.
    3) Else save without compressing.
    4) Or if the compressed version is larger, save without compressing then too.
    """
    try:
        compressed_data = zst_mod.compress(data)
        compression_type = 8
        compressed_ok = True
    except OSError:
        if HAVE_BZ2:
            if not bz2_announced:
                sys.stderr.write('%s: warning: falling back to bzip2 compression due to lack of xz\n' % sys.argv[0])
                bz2_announced = True
            compressed_data = bz2_mod.compress(data)
            compression_type = 5
            compressed_ok = True
        else:
            compressed_ok = False

    if not compressed_ok or len(data) < len(compressed_data):
        # Many strings don't compress - they instead get larger.  So we catch that and allow them to increase
        # by 2 bytes only.
        result = constants_mod.Constants.b_onenewline + data
    else:
        result = \
            helpers.string_to_binary('%d' % compression_type) + \
            constants_mod.Constants.b_newline + \
            compressed_data

    binary_result = helpers.string_to_binary(result)

    return binary_result


def decompress_string(compressed_data, zero_length_ok=False):
    """Uncompress a string."""
    memory_file = stringio.StringIO(compressed_data)
    compression_type = memory_file.readline().rstrip()
    remainder = memory_file.read()
    if compression_type == constants_mod.Constants.b_8:
        decompressed_data = zst_mod.decompress(remainder)
    elif compression_type == constants_mod.Constants.b_7:
        decompressed_data = xz_mod.decompress(remainder)
    elif compression_type == constants_mod.Constants.b_5:
        decompressed_data = bz2_mod.decompress(remainder)
    elif compression_type == constants_mod.Constants.b_1:
        decompressed_data = remainder
    elif zero_length_ok and compression_type == helpers.empty_bytes:
        decompressed_data = helpers.empty_bytes
    else:
        raise ValueError('Did not get a valid compression type from compressed_data')
    return decompressed_data
