#!/usr/bin/env python

"""
Implements a dictionary-like database with a degree of persistence.

On open, we read the database into a dictionary.
We mutate the dictionary in memory.
Then on close, we write the dictionary back to disk.

Has the advantage of being in Pure Python, so it works on about any
Python interpreter one cares to consider.
"""

import os
import sys
import errno

import base255
import bufsock
from touch import touch

REAL_OPEN = open
MAIN_OPEN = bufsock.rawio
NULL_BYTE = bytes([0])


def string_to_binary(string):
    """Convert a text string (or binary string type) to a binary string type."""
    if isinstance(string, str):
        return string.encode('latin-1')
    return string


DOT_TEMP = string_to_binary('.temp')


def safe_rename(backup_filename, regular_filename):
    """Rename backup_filename to regular_filename."""
    # This is copied verbatim from backshift

    # Deal with the fact that CIFS may EEXIST when renaming to a file that already exists.
    unlink_and_rename = False

    try:
        os.rename(backup_filename, regular_filename)
    except (OSError, IOError) as extra:
        if extra.errno == errno.EEXIST:
            unlink_and_rename = True
        else:
            sys.stderr.write('Got errno %s while trying to rename %s to %s\n' % (extra.errno, backup_filename, regular_filename))
            raise

    if unlink_and_rename:
        os.unlink(regular_filename)
        os.rename(backup_filename, regular_filename)


class error(Exception):
    """An exception to raise when we have problems."""

    pass


def open(filename, flag='rb', mode=6 * 64 + 6 * 8 + 6, backend_open=MAIN_OPEN):
    """Open a dohdbm database."""
    # pylint: disable=W0622
    # W0622: We want to redefine open for consistency with other python nosql databases
    return Dohdbm(filename, flag, mode, backend_open)


def _generate_key_value_pairs(file_):
    """Read key-value pairs from disk."""
    convenient_file = bufsock.bufsock(file_, chunk_len=2**23)
    to_next_null = convenient_file.readto(NULL_BYTE)
    minus_trailing_null = to_next_null.rstrip(NULL_BYTE)
    number_of_pairs = base255.base255_to_number(minus_trailing_null)
    # we iterate manually to avoid needing to define our own range generator
    pairno = 0
    while pairno < number_of_pairs:
        key_length = base255.base255_to_number(convenient_file.readto(NULL_BYTE).rstrip(NULL_BYTE))
        key = convenient_file.read(key_length)
        value_length = base255.base255_to_number(convenient_file.readto(NULL_BYTE).rstrip(NULL_BYTE))
        value = convenient_file.read(value_length)
        yield (key, value)
        pairno += 1


class Dohdbm(object):
    # pylint: disable=R0902,R0912
    # R0902: We want a bunch of instance attributes
    # R0912: We need some branches I guess :( - otherwise we end up setting instance attributes from something other than __init__
    """A class implementing a simple database."""

    def __init__(self, filename, flag='r', mode=6 * 64 + 6 * 8 + 5, backend_open=MAIN_OPEN):
        """Initialize."""
        self.dirty = False
        self.filename = filename
        assert len(flag) in [1, 2]
        self.flag0 = flag[0]
        assert self.flag0 in ['r', 'w', 'c', 'n']
        if flag[1:]:
            self.flag1 = flag[1]
            assert self.flag1 in ['f', 's', 'u', 'b']
        else:
            self.flag1 = ''
        # actually, we always treat our keys and values as binary, irrespective of the "b" flag
        assert self.flag1 in ['', 'b']
        self.mode = mode
        self.backend_open = backend_open
        should_read_file = True
        self.file_ = None
        if self.flag0 == 'r':
            self.file_ = self.backend_open(filename, 'rb')
            should_read_file = True
        elif self.flag0 == 'w':
            try:
                self.file_ = self.backend_open(filename, 'rb')
            except (OSError, IOError):
                should_read_file = False
                touch(filename)
        elif self.flag0 == 'c':
            try:
                self.file_ = self.backend_open(filename, 'rb')
            except (OSError, IOError):
                self._create_empty(filename, mode)
                self.file_ = self.backend_open(filename, 'rb')
        elif self.flag0 == 'n':
            should_read_file = False
            self._create_empty(filename, mode)
            self.file_ = self.backend_open(filename, 'rb', mode)
        else:
            raise AssertionError("Invalid flag: %s" % self.flag0)
        self.dict_ = {}
        if should_read_file:
            for key, value in _generate_key_value_pairs(self.file_):
                self.dict_[key] = value
        if self.file_ is not None:
            self.file_.close()
        self.is_open = True

    def _create_empty(self, filename, mode):
        """Create an empty "database"."""
        tempfile = self.backend_open(filename, 'wb', mode)
        tempfile.write(base255.number_to_base255(0) + NULL_BYTE)
        tempfile.close()

    def _error_if_not_open(self):
        """Raise an error if the database isn't currently open."""
        if self.is_open:
            return
        else:
            raise error("Database is not open")

    def _error_if_not_readwrite(self):
        """Raise an error if the database isn't currently open."""
        if self.flag0 in ['w', 'c', 'n']:
            return
        else:
            raise error("Database is not read/write")

    def __len__(self):
        """Return the number of items in the database."""
        self._error_if_not_open()
        return len(self.dict_)

    def __getitem__(self, key):
        """Return the value in the database associated with key."""
        self._ensure_bytes(key)
        self._error_if_not_open()
        return self.dict_[key]

    def __setitem__(self, key, value):
        """Associate value with key in the database."""
        if self.flag0 == 'r':
            raise error('Attempt to modify a readonly database')
        self.dirty = True
        self._ensure_bytes(key)
        self._ensure_bytes(value)
        self._error_if_not_open()
        self._error_if_not_readwrite()
        self.dict_[key] = value

    def __delitem__(self, key):
        """Delete the key-value pair indexed by key in the database."""
        if self.flag0 == 'r':
            raise error('Attempt to modify a readonly database')
        self.dirty = True
        self._ensure_bytes(key)
        self._error_if_not_open()
        self._error_if_not_readwrite()
        del self.dict_[key]

    def __iter__(self):
        """Generate all keys in the database."""
        self._error_if_not_open()
        for key in self.dict_:
            yield key

    def __contains__(self, key):
        """Return True iff key is in the database."""
        self._ensure_bytes(key)
        self._error_if_not_open()
        return key in self.dict_

    def sync(self):
        """Flush the database to disk."""
        if self.flag0 == 'r':
            # Nothing to do - this is a readonly database.
            return
        self._error_if_not_open()
        self._error_if_not_readwrite()
        temp_filename = string_to_binary(self.filename) + DOT_TEMP
        file_ = self.backend_open(temp_filename, 'wb', self.mode)
        file_.write(base255.number_to_base255(len(self.dict_)) + NULL_BYTE)
        for key in self.dict_:
            # there's a faster way, but it's not as portable
            value = self.dict_[key]
            file_.write(base255.number_to_base255(len(key)) + NULL_BYTE)
            file_.write(key)
            file_.write(base255.number_to_base255(len(value)) + NULL_BYTE)
            file_.write(value)
        file_.close()
        safe_rename(temp_filename, self.filename)
        self.dirty = False

    def close(self):
        """Close a database: sync it to disk and mark it closed."""
        # We're supposed to be idempotent, apparently
        if self.is_open:
            if self.flag0 == 'r':
                assert not self.dirty
            if self.dirty:
                self.sync()
            self.is_open = False

    def keys(self):
        """Return the keys in the database."""
        return self.dict_.keys()

    def items(self):
        """Return the items, AKA the key-value pairs, in the database."""
        return self.dict_.items()

    @classmethod
    def _ensure_bytes(cls, string):
        """Make sure a key or value is of the bytes type."""
        if isinstance(string, bytes):
            return
        else:
            raise AssertionError('dohdbm called with non-bytes key and/or value: {}'.format(type(string)))

#    def __enter__(self, *dummy):
#        return self
#
#    def __exit__(self, type_, value, traceback_):
#        if value is None:
#            self.close()
#            return True
#        else:
#            return False
