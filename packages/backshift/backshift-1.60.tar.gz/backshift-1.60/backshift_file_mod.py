#!/usr/bin/env python

"""
An abstract representation of a file of various kinds, including directories.

Used as a bridge between stat-data and the repo, or the repo and tar output.
"""

# pylint: disable=simplifiable-if-statement

import os
import sys
import stat
import time

import backshift_os_mod
import constants_mod
import helpers
import metadata_mod


def make_used(var):
    """Persuade linters that var is 'used'."""
    assert True or var


def perms_string(bits, weird_x=None):
    """Convert a 3 bit quantity to a more human-readable description - EG, 'rwx'."""
    list_ = []
    if bits & 4:
        list_.append('r')
    else:
        list_.append('-')
    if bits & 2:
        list_.append('w')
    else:
        list_.append('-')
    if bits & 1:
        if weird_x is not None:
            list_.append(weird_x)
        else:
            list_.append('x')
    else:
        list_.append('-')
    return ''.join(list_)


class Skipped(Exception):
    """An exception to raise when we are passed a file of an invalid (unknown) type, including unix domain sockets."""

    pass


class Benign_skipped(Skipped):
    """An exception to raise when we we skip something unimportant, like a unix domain socket."""

    pass


class Unknown_skipped(Skipped):
    """An exception to raise when we skip something that could conceivably be important - IOW, an unknown file type."""

    pass


class Problematic_skipped(Skipped):
    """An exception to raise when we we skip something we know is important."""

    pass


def weird_bit(mode, bit, character):
    """Deal with sticky, setgid and setuid bits."""
    if mode & bit:
        weird_x = character
    else:
        weird_x = None
    return weird_x


def get_can_do_device_files():
    """Return True iff it looks like the Python interpreter has the necessary support to backup device files."""
    if not hasattr(os, 'major'):
        return False
    if not hasattr(os, 'minor'):
        return False
    stat_buf = os.stat('/')
    return hasattr(stat_buf, 'st_rdev')


class Backshift_file(object):
    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods
    """
    An abstract representation of a file of various kinds, including directories.

    Used as a bridge between stat-data and the repo, or the repo and tar output.
    """

    max_digits = 1

    kind_dict = {}
    kind_dict[constants_mod.Constants.b_block_device] = 'b'
    kind_dict[constants_mod.Constants.b_character_device] = 'c'
    kind_dict[constants_mod.Constants.b_directory] = 'd'
    kind_dict[constants_mod.Constants.b_fifo] = 'p'
    kind_dict[constants_mod.Constants.b_hardlink] = 'h'
    kind_dict[constants_mod.Constants.b_regular_file] = '-'
    kind_dict[constants_mod.Constants.b_symlink] = 'l'

    def __init__(self, repo, file_, filename, verbose=False):
        """Initialize our dictionary to something indicating that all attributes missing."""
        self.dict_ = {}
        for key in metadata_mod.File_attributes.dict_:
            self.dict_[key] = None

        self.repo = repo
        self.filename = filename

        self.type_ = None

        # now fill in the attributes we actually have
        if hasattr(os, 'stat_result') and isinstance(file_, os.stat_result):
            # We're receiving a file from stat - probably during a backup
            speed = self.init_from_lstat_result(lstat_result=file_)
            self.repo.speeds.add_speed(speed)
            if verbose:
                os.write(sys.stdout.fileno(), helpers.string_to_binary('%s ' % speed))
        else:
            # otherwise we assume this is a file(-like object), and fill in from that
            self.init_from_string(file_)

    def init_from_lstat_result(self, lstat_result, can_do_device_files=get_can_do_device_files()):
        """Save a file in the repository."""
        if stat.S_ISREG(lstat_result.st_mode):
            self.type_ = constants_mod.Constants.b_regular_file
        elif stat.S_ISLNK(lstat_result.st_mode):
            self.type_ = constants_mod.Constants.b_symlink
        elif stat.S_ISDIR(lstat_result.st_mode):
            self.type_ = constants_mod.Constants.b_directory
        elif stat.S_ISCHR(lstat_result.st_mode):
            if can_do_device_files:
                self.type_ = constants_mod.Constants.b_character_device
            else:
                raise Problematic_skipped('%s: skipping character device %s because this python does not support it' %
                                          (sys.argv[0], self.filename))
        elif stat.S_ISBLK(lstat_result.st_mode):
            if can_do_device_files:
                self.type_ = constants_mod.Constants.b_block_device
            else:
                tuple_ = (sys.argv[0], self.filename)
                raise Problematic_skipped('%s: skipping block device %s because this python does not support it' % tuple_)
        elif stat.S_ISFIFO(lstat_result.st_mode):
            self.type_ = constants_mod.Constants.b_fifo
        elif stat.S_ISSOCK(lstat_result.st_mode):
            # we can safely ignore unix domain sockets - these are created by processes, and will be recreated by them as needed.
            raise Benign_skipped('%s: skipping unix domain socket %s' % (sys.argv[0], self.filename))
        else:
            raise Unknown_skipped('%s: %s is of an unrecognized file type' % (sys.argv[0], self.filename))

        speed = self.process_from_lstat(lstat_result)
        return speed

    def process_from_lstat(self, lstat_result):
        """Deal with the metadata fields."""
        speed = 'stat'

        if self.type_ in metadata_mod.File_types.dict_:
            for metadatum in metadata_mod.File_types.dict_[self.type_]:
                self.dict_[metadatum.field] = metadatum.get_from_stat(self.filename, lstat_result, metadatum.field)
            assert constants_mod.Constants.b_hash in self.dict_
            if self.dict_.get(constants_mod.Constants.b_regular_file):
                speed = self.repo.save_chunks(lstat_result, self.filename, self.dict_)
        else:
            sys.stderr.write('%s: %s not in %s\n' % (sys.argv[0], self.type_, metadata_mod.File_types.dict_.keys()))

        return '%*s' % (constants_mod.Constants.file_type_width, speed)

    def init_from_string(self, file_):
        """Construct (initialize, really) a Backshift file from the file like object we get from reading a file's metadata."""
        for line in file_.split(constants_mod.Constants.b_newline):
            fields = line.split()
            if not fields:
                # this was a blank line - don't stress about it
                continue
            if not fields[1:]:
                raise AssertionError('%s: Too few fields in %s of %s' % (sys.argv[0], fields, self.filename))
            if fields[2:]:
                raise AssertionError('%s: Too many fields in %s of %s' % (sys.argv[0], fields, self.filename))
            key = fields[0]
            if key not in metadata_mod.File_attributes.dict_:
                raise AssertionError('%s: Invalid key %s of %s' % (sys.argv[0], key, self.filename))
            if key == constants_mod.Constants.b_hash:
                # hashes can legitimately be repeated
                cooked_value = metadata_mod.File_attributes.dict_[constants_mod.Constants.b_hash].get_from_fields(fields)
                if key in self.dict_ and self.dict_[key] is not None:
                    self.dict_[key].append(cooked_value)
                else:
                    self.dict_[key] = [cooked_value]
            else:
                # all others most be unique for a given dictionaryn key
                if key in self.dict_ and self.dict_[key] is not None:
                    raise AssertionError('%s: Field %s occurs more than once in %s' % (sys.argv[0], key, self.filename))
                else:
                    self.dict_[key] = metadata_mod.File_attributes.dict_[key].get_from_fields(fields)
        self.init_string_set_type()

    def init_string_set_type(self):
        """Just set the type - for when constructing from init_from_string."""
        for what_type in ['regular_file', 'symlink', 'directory', 'character_device', 'block_device', 'fifo']:
            binary_what_type = helpers.string_to_binary(what_type)
            if binary_what_type in self.dict_ and self.dict_[binary_what_type]:
                self.type_ = binary_what_type
                break
        else:
            sys.stderr.write('%s: %s is of an unrecognized file type\n' % (sys.argv[0], self.filename))
            return

    def __len__(self):
        """Return length."""
        return len(self.dict_)

    # we intentionally aren't providing __setitem__ - there's no need
    def __getitem__(self, key):
        """Look up key in dict."""
        return self.dict_[key]

    def __contains__(self, key):
        """Return True if key in dict."""
        return key in self.dict_[key]

    def as_string(self):
        """Format this file's metadata as a string for storage in some sort of database."""
        keys = [helpers.string_to_binary(key) for key in self.dict_]
        keys.sort()
        list_ = []
        blank = constants_mod.Constants.b_blank
        minus = constants_mod.Constants.b_minus
        for key in keys:
            if self.dict_[key] is not None:
                if key == constants_mod.Constants.b_hash:
                    # The hashes are in a list.  The others are all just scalars.
                    for hash_ in self.dict_[key]:
                        if isinstance(hash_, (bytes, str)):
                            string = key + blank + helpers.string_to_binary(hash_.rstrip().replace(' ', '-'))
                        elif isinstance(hash_, tuple):
                            string = \
                                key + \
                                blank + \
                                helpers.string_to_binary(hash_[0]) + \
                                minus + \
                                helpers.string_to_binary(str(hash_[1]))
                        else:
                            raise ValueError('hash_ is not a bytes_type or tuple: %s' % type(hash_))
                        list_.append(string)
                else:
                    value = self.dict_[key]
                    if isinstance(value, bytes):
                        binary = value
                    else:
                        binary = helpers.string_to_binary(str(value))
                    string = key + blank + binary
                    list_.append(string)
        return constants_mod.Constants.b_newline.join(list_)

    def get_username(self):
        """If the user exists, return the username - otherwise return uid."""
        try:
            pwent = backshift_os_mod.my_getpwnam(helpers.binary_to_string(self.dict_[constants_mod.Constants.b_owner]))
        except KeyError:
            return '%d' % self.dict_[constants_mod.Constants.b_st_uid]
        else:
            make_used(pwent)
            return helpers.binary_to_string(self.dict_[constants_mod.Constants.b_owner])

    def get_groupname(self):
        """If the group exists, return the group - otherwise return gid."""
        try:
            grent = backshift_os_mod.my_getgrnam(helpers.binary_to_string(self.dict_[constants_mod.Constants.b_group]))
        except KeyError:
            return '%d' % self.dict_[constants_mod.Constants.b_st_gid]
        else:
            make_used(grent)
            return helpers.binary_to_string(self.dict_[constants_mod.Constants.b_group])

    def get_real_length(self):
        """Compute the real length of the file (as opposed to what's in st_size, by adding up the hash keys' lengths."""
        total = 0
        binary_hash = constants_mod.Constants.b_hash
        if binary_hash in self.dict_ and self.dict_[binary_hash] is not None:
            for hash_entry in self.dict_[binary_hash]:
                if hash_entry[1:] and not hash_entry[2:]:
                    current = int(hash_entry[1])
                    total += current
                else:
                    raise AssertionError('Bad number of entries in hash_entry 2-tuple: %s' % hash_entry)
        return total

    def to_tar_tf(self):
        """Generate a "tar tf"-like description of this file - That is, just list the filename."""
        # ./tests/40-smoke/Makefile
        # ./tests/66-rcm-perf/
        return helpers.string_to_binary(self.filename)

    def to_tar_tvf(self, hardlink_data):
        """Generate a "tar tvf"-like description of this file."""
        # -rw-r--r-- dstromberg/dstromberg       750 2    -02-08 14:28 ./tests/40-smoke/Makefile
        # drwxr-xr-x dstromberg/dstromberg         0 2    -04-03 10:37 ./tests/66-rcm-perf/
        list_ = []

        derived_type = self.type_

        prior_filename = None

        if derived_type == constants_mod.Constants.b_regular_file:
            deviceno = self.dict_[constants_mod.Constants.b_st_dev]
            inodeno = self.dict_[constants_mod.Constants.b_st_ino]
            filename = self.filename
            prior_filename = hardlink_data.prior_file_for_hardlink(deviceno, inodeno, filename)
            if prior_filename:
                # this is a hardlink
                derived_type = helpers.string_to_binary('hardlink')

        if derived_type in Backshift_file.kind_dict:
            list_.append(Backshift_file.kind_dict[derived_type])
        else:
            raise ValueError('Unrecognized filetype: %s' % derived_type)

        mode = self.dict_[constants_mod.Constants.b_st_mode]
        weird_x = weird_bit(mode, stat.S_ISUID, 's')
        list_.append(perms_string((mode & (7 * 64)) // (8 * 8), weird_x=weird_x))
        weird_x = weird_bit(mode, stat.S_ISGID, 's')
        list_.append(perms_string((mode & (7 * 8)) // 8, weird_x=weird_x))
        weird_x = weird_bit(mode, stat.S_ISVTX, 't')
        list_.append(perms_string(mode & 7, weird_x=weird_x))

        list_.append(' ')

        list_.append('%s/%s' % (self.get_username(), self.get_groupname()))

        list_.append(' ')

        if derived_type == constants_mod.Constants.b_character_device:
            length = '%s,%s' % (
                self.dict_[constants_mod.Constants.b_character_major],
                self.dict_[constants_mod.Constants.b_character_minor],
            )
        elif derived_type == constants_mod.Constants.b_block_device:
            length = '%s,%s' % (
                self.dict_[constants_mod.Constants.b_block_major],
                self.dict_[constants_mod.Constants.b_block_minor],
            )
        elif derived_type in [constants_mod.Constants.b_symlink, constants_mod.Constants.b_hardlink]:
            length = '0'
        else:
            length = '%d' % self.get_real_length()

        num_digits = len(length)
        if num_digits > Backshift_file.max_digits:
            Backshift_file.max_digits = num_digits
        format_string = '%%%ds' % Backshift_file.max_digits
        list_.append(format_string % length)

        list_.append(' ')

        list_.append(time.strftime('%Y-%m-%d %H:%M', time.localtime(self.dict_[constants_mod.Constants.b_st_mtime])))

        list_.append(' ')

        list_.append(helpers.binary_to_string(self.filename))

        self.tail_special(list_, derived_type, prior_filename)

        stuff = helpers.string_to_binary(''.join(list_))
        # GNU tar doubles backslashes, so we do also
        return stuff.replace(b'\\', b'\\\\')

    def tail_special(self, list_, derived_type, prior_filename):
        """Deal with some special cases near the end of a tvf line."""
        if derived_type == constants_mod.Constants.b_directory:
            list_.append('/')

        if derived_type == constants_mod.Constants.b_symlink:
            list_.append(' -> ')
            target = self.dict_[constants_mod.Constants.b_link_target]
            bts_target = helpers.binary_to_string(target)
            list_.append(bts_target)

        if derived_type == constants_mod.Constants.b_hardlink:
            list_.append(' link to ')
            assert prior_filename is not None
            target = prior_filename
            bts_target = helpers.binary_to_string(target)
            list_.append(bts_target)
