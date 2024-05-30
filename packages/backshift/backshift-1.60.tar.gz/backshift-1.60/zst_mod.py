#!/usr/bin/env python3

"""Provide zstandard compression and uncompression in one of a few ways."""

# <module 'zst_zstd' from '/home/dstromberg/src/home-svn/zst_mod/trunk/zst_zstd.py'> 2.3933606147766113
# <module 'zst_zstandard' from '/home/dstromberg/src/home-svn/zst_mod/trunk/zst_zstandard.py'> 0.9748928546905518
# <module 'zst_pyzstd' from '/home/dstromberg/src/home-svn/zst_mod/trunk/zst_pyzstd.py'> 1.2322025299072266
#
# IOW, there's a pretty big performance difference.

try:
    from zst_zstandard import compress, decompress
except ImportError:
    got_one = False
else:
    got_one = True

if not got_one:
    try:
        from zst_pyzstd import compress, decompress
    except ImportError:
        got_one = False
    else:
        got_one = True

if not got_one:
    try:
        from zst_zstd import compress, decompress
    except ImportError:
        got_one = False
    else:
        got_one = True

if not got_one:
    raise ImportError("Failed to get a zstd module")
