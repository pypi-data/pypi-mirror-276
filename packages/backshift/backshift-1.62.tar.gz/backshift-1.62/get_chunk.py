#!/usr/bin/python3

"""Read a chunk, write its data to stdout.  We do not verify - that can be done with a pipe to sha256."""

import re
import sys

import repo_mod
import chunk_mod
import helpers


def get_hash_len(sample_hash=repo_mod.get_hash(helpers.null_byte)):
    """Calculate the length of a good hash."""
    return len(sample_hash)


def get_chunk(hash_string):
    """Get a single chunk and write its value to stdout. Here for debugging purposes."""
    required_hash_len = get_hash_len()

    bad = False

    if hash_string == '':
        sys.stderr.write('%s: --get-chunk is a required option\n' % (sys.argv[0], ))
        bad = True

    if len(hash_string) != required_hash_len:
        sys.stderr.write('%s: --get-chunk has an invalid length\n' % (sys.argv[0], ))
        bad = True

    regex = re.compile('^[0-9a-f]{%s}$' % required_hash_len)
    match = regex.match(hash_string)
    if not match:
        sys.stderr.write('%s: --get-hash must specify a %s character, lowercase, hexadecimal string\n' % (
            sys.argv[0],
            required_hash_len,
        ))
        bad = True

    if bad:
        sys.stderr.write('%s: preflight check failed\n' % (sys.argv[0], ))
        sys.exit(1)

    chunk = chunk_mod.Chunk(hash_string)
    data = chunk.read_chunk()

    sys.stdout.write(helpers.binary_to_string(data))
