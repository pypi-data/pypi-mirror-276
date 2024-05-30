#!/usr/bin/env python

"""
A module for reading and writing (sometimes) compressed files.

Note that everything is stored in memory - in fact, sometimes there'll
be the uncompressed data and compressed data in memory at the same time.
So this is not for huge files, but works fine for tens or even hundreds
of megabytes.
"""

import bufsock
import compressed_string_mod
import constants_mod
import helpers
import stringio


class Compressed_file(object):
    """A class for dealing with compressed files."""

    # pylint: disable=R0913
    # R0913: We need a few arguments
    def __init__(self, filename, mode, perms=None, start_empty=False, zero_length_ok=False):
        """Initialize."""
        self.filename = filename
        self.mode = mode
        # FIXME: We ignore perms - that's pretty safe for backshift, but should be examined if reused in other projects
        _ = perms
        self.start_empty = start_empty
        if self.mode not in ['r', 'rb', 'w', 'wb']:
            raise AssertionError('Illegal mode: %s\n' % mode)
        if self.mode.startswith('r'):
            self.reading = True
            self.writing = False
            raw_file = bufsock.rawio(filename, mode)
            self.file_ = bufsock.bufsock(raw_file, chunk_len=constants_mod.Constants.block_size)
            data = self.file_.read()
            self.memory_file = stringio.StringIO(compressed_string_mod.decompress_string(data, zero_length_ok))
        elif self.mode.startswith('w'):
            self.reading = False
            self.writing = True
            file_ = open(self.filename, self.mode)
            self.memory_file = stringio.StringIO()
            if self.start_empty:
                # If requested, then we write an "empty" compressed byte sequence to the file - to deter errors from
                # decompressing 0 length files.
                # raw_file = bufsock.rawio(filename, mode)
                # file_ = bufsock.bufsock(raw_file, chunk_len=2 ** 12)
                compressed_data = compressed_string_mod.compress_string(helpers.null_byte)
                file_.write(compressed_data)
                file_.flush()
                file_.seek(0)
            # We assign file_ to self.file_ late like this, to avoid confusing pylint's type inference
            self.file_ = file_
        else:
            raise ValueError('Compressed_file: Mode does not start with r or w?')

    def read(self, length=None):
        """Read bytes from our 'file'."""
        if self.reading:
            if length is None:
                return self.memory_file.read()
            return self.memory_file.read(length)
        else:
            raise IOError('Attempted to read from a write-only Compressed_file')

    def write(self, data):
        """Write bytes to our 'file'."""
        if self.writing:
            self.memory_file.write(data)
        else:
            raise IOError('Attempted to write to a read-only Compressed_file')

    def close(self):
        """Close the file."""
        if self.writing:
            self.memory_file.seek(0)
            data = self.memory_file.read()
            self.memory_file.close()

            compressed_data = compressed_string_mod.compress_string(data)

            self.file_.write(compressed_data)

        self.file_.close()

        # If reading, there's nothing to do - we read the whole thing in the initializer
