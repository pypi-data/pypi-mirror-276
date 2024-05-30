#!/usr/bin/python

"""
Manage the chunk hierarchy.

Holds the contents of files, though for large files that'll be split up into multiple smaller chunks
"""

import errno
import os
import sys

import backshift_os_mod
import compressed_file_mod
import constants_mod
import dirops_mod
import helpers


def is_jython(is_it=(sys.platform.startswith('java'))):
    """Return True iff we're on Jython."""
    return is_it

# def pieces(string):
#    """
#    Divide up a string into pieces - 2 characters, then 3 characters, then 5 characters, etc.
#    We use fibonnaci numbers * 4, excluding the first two numbers: 0 and 1.
#    """
#    len_string = len(string)
#    size_so_far = 0
#    for fibno, piece_len in enumerate(fib * 4 for fib in fibonnaci_sequence()):
#        if fibno < 2:
#            continue
#        if size_so_far < len_string:
#            piece = string[size_so_far:size_so_far + piece_len]
#            yield piece
#            size_so_far += len(piece)
#        else:
#            break


def pieces(string):
    """Divide up a string into pieces."""
    len_string = len(string)
    size_so_far = 0
    for piece_len in ad_hoc_sequence():
        if size_so_far < len_string:
            piece = string[size_so_far:size_so_far + piece_len]
            yield piece
            size_so_far += len(piece)
        else:
            break


def ad_hoc_sequence():
    """Produce a less pretty sequence of directory sizes. It seems to give a good growth rate."""
    yield 5
    yield 6
    while True:
        yield 54

# def powers_of_2_25():
#    """Generate the powers of 2.25"""
#    power = 1
#    while True:
#        yield int(power)
#        power *= 2.25

# Having an actual practical use for fibonacci numbers feels really cool, but I'm happier with powers of 2.25 now.
# def fibonnaci_sequence():
#    """Return the fibonacci sequence"""
#    first = 0
#    yield first
#    second = 1
#    yield second
#    while True:
#        first, second = second, first+second
#        yield second


class Chunk(object):
    """Perform operations (read, write, update timestamp) on a chunk (of a file)."""

    # This one is filled in by repo_mod
    canonical_hostname = None

    # We compute this one from the one above
    bytes_canonical_hostname = None

    prefix = constants_mod.Constants.b_chunks

    def __init__(self, digest):
        """Initialize Chunk object."""
        if Chunk.bytes_canonical_hostname is None:
            Chunk.bytes_canonical_hostname = helpers.string_to_binary(Chunk.canonical_hostname)

        nybble_paths = [helpers.string_to_binary(piece) for piece in pieces(digest)]
        intervening_dirs = nybble_paths[:-1]
        self.filename = nybble_paths[-1]
        self.all_dirs_list = [Chunk.prefix] + intervening_dirs
        self.all_dirs_string = os.path.join(*self.all_dirs_list)
        self.path = os.path.join(self.all_dirs_string, self.filename)

    def write_or_touch_chunk(self, chunk_bytes):
        """Write a chunk_bytes if it doesn't exist, or just update the mtime and atime if it does."""
        try:
            self.update_timestamp()
        except (OSError, IOError) as utime_extra:
            # Recent Pypy3 (pypy3-5.5.0, pypy3-5.7.1) likes to give ENOTTY instead of ENOENT
            # https://bitbucket.org/pypy/pypy/issues/2548/pypy3-returns-inappropriate-errno-for
            # Bug fixed, but it could be a while until it's rolled up into a (beta) release.
            if utime_extra.errno == errno.ENOENT:
                # The file doesn't exist, so create it
                dirops_mod.my_mkdir(self.all_dirs_list)
                pid = helpers.string_to_binary(str(os.getpid()))
                list_ = [
                    self.path,
                    constants_mod.Constants.b_underscore,
                    Chunk.bytes_canonical_hostname,
                    constants_mod.Constants.b_underscore,
                    pid,
                ]
                temp_filename = helpers.empty_bytes.join(list_)
                compressed_file = compressed_file_mod.Compressed_file(temp_filename, 'wb')
                compressed_file.write(chunk_bytes)
                compressed_file.close()
                backshift_os_mod.safe_rename(temp_filename, self.path)
                return len(chunk_bytes)
            else:
                # This was an OSError or IOError, but not an ENOENT (file not found) or ENOTTY (inappropriate ioctl for device)
                sys.stderr.write('Got a weird errno updating utime for {}: {}\n'.format(self.path, utime_extra.errno))
                raise
        else:
            return 0

    def read_chunk(self):
        """Read a chunk_bytes back from the chunk."""
        compressed_file = compressed_file_mod.Compressed_file(self.path, 'rb')
        data = compressed_file.read()
        compressed_file.close()
        return data

    # def update_timestamp(self, am_i_jython=is_jython()):
    def update_timestamp(self):
        """Update the timestamp on a chunk (hash)."""
        # We intentionally don't mkdir - the directories and file should already exist.
        # If they don't, that's something we should traceback or give an error about.
#        if am_i_jython:
#            # On Jython 2.5.2 r7288, os.utime fails to raise an OSError if the file doesn't exist
#            # So instead, we first open for reading - if the file's not there, this'll raise an OSError
#            # with ENOENT.  If it succeeds, then we open the file for rb+ - this'll update the file's
#            # timestamp.
#            open(self.path, 'r').close()
#            open(self.path, 'rb+').close()
#        else:

        # Jython 2.5.3b1 behaves itself :)
        os.utime(self.path, None)


def finalize():
    """Close the databases."""
    pass
