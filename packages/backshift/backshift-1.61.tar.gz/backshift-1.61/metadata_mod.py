#!/usr/bin/env python

"""Describes and converts various metadata and metadata representations."""

import os
import sys

import backshift_os_mod
import constants_mod
import escape_mod
import helpers


class Metadata(object):
    # pylint: disable=R0903
    # R0903: We don't need any more public methods than this
    """Contains one metadata attribute of a file."""

    def __init__(self, field, get_from_stat, get_from_fields):
        """Initialize."""
        self.field = field
        self.get_from_stat = get_from_stat
        self.get_from_fields = get_from_fields


def get_int_from_fields(fields):
    """Extract an integer field from a repo line."""
    assert fields[1:] and not fields[2:]
    return int(fields[1])


def get_float_from_fields(fields):
    """Extract a floating point field from a repo line."""
    assert fields[1:] and not fields[2:]
    return float(fields[1])


def get_string_from_fields(fields):
    """Extract a string field from a repo line."""
    assert fields[1:] and not fields[2:]
    # it's already a string
    return fields[1]


def get_escaped_string_from_fields(fields):
    """Extract a string field from a repo line."""
    assert fields[1:] and not fields[2:]
    # it's already a string
    return escape_mod.unescape(fields[1])


def get_bool_from_fields(fields):
    """Extract a boolean from a list of fields."""
    if fields[1] == constants_mod.Constants.b_true:
        return True
    elif fields[1] == constants_mod.Constants.b_false:
        return False
    else:
        raise ValueError('Boolean not True or False: %s' % fields[1])


def undefined(stat_buf, field):
    """Extract an undefined field from a stat - used for derived fields."""
    helpers.make_used([stat_buf, field])
    raise NotImplementedError


def get_field_on_stat(filename, stat_buf, field):
    """Just pull out a field - not much to do with types here, because stat returns things reasonably to begin with."""
    helpers.make_used(filename)
    value = getattr(stat_buf, helpers.binary_to_string(field))
    return value


def always_true(filename, stat_buf, field):
    """Just always return True, for things that are single-field like directory or regular_file."""
    helpers.make_used([filename, stat_buf, field])
    return True

# Believe it or not, both Windows and Linux allow blanks in usernames and groupnames.  So we escape them.


def get_group_on_stat(filename, stat_buf, field):
    """Look up the group name (not just the gid) - if none, return #gid."""
    helpers.make_used([filename, field])
    gid = stat_buf.st_gid
    try:
        grp_ent = backshift_os_mod.my_getgrgid(gid)
    except KeyError:
        group = '%d' % gid
    else:
        group = grp_ent.gr_name
    return escape_mod.escape(group)


def get_owner_on_stat(filename, stat_buf, field):
    """Look up the username (not just the uid) - if none, return #uid."""
    helpers.make_used([filename, field])
    uid = stat_buf.st_uid
    try:
        pw_ent = backshift_os_mod.my_getpwuid(uid)
    except KeyError:
        user = '%d' % uid
    else:
        user = pw_ent.pw_name
    return escape_mod.escape(user)


def init_hashes_on_stat(filename, stat_buf, field):
    """Just give an initial empty list for the hashes - we'll handle them separately/specially."""
    helpers.make_used([filename, stat_buf, field])
    return []


def get_link_target_on_stat(filename, stat_buf, field):
    """Return the link target of the file in question, encoded in base64 so we needn't worry about whitespace issues."""
    helpers.make_used([stat_buf, field])
    try:
        not_yet_escaped = os.readlink(filename)
    except OSError:
        sys.stderr.write('Symlink disappeared? %s\n' % filename)
        not_yet_escaped = constants_mod.Constants.b_readlink_failed
    escaped = escape_mod.escape(not_yet_escaped)
    return escaped


def get_hashes_from_fields(fields):
    """Get the hashes from a fields line - actually, we get the hashes and the lengths of the chunks they're hashes of."""
    subfields = fields[1].split(constants_mod.Constants.b_minus)
    assert subfields[1:] and not subfields[2:]
    return (subfields[0], int(subfields[1]))


def get_st_rdev(stat_buf):
    """Extract st_rdev (st_dev doesn't count) from an os.stat return."""
    return stat_buf.st_rdev


def get_major_on_stat(filename, stat_buf, field):
    """Get the major device number for a device."""
    helpers.make_used([filename, field])
    return os.major(get_st_rdev(stat_buf))


def get_minor_on_stat(filename, stat_buf, field):
    """Get the minor device number for a device."""
    helpers.make_used([filename, field])
    return os.minor(get_st_rdev(stat_buf))


class File_attributes(object):
    # pylint: disable=W0232,R0903
    # W0232: We don't need an __init__ method
    # R0903: We don't need any public methodes
    """Contains the various metadata attributes a file might have - as class variables."""

    cmc = constants_mod.Constants

    dict_ = {}
    dict_[cmc.b_block_device] = Metadata(cmc.b_block_device, always_true, get_bool_from_fields)
    dict_[cmc.b_block_major] = Metadata(cmc.b_block_major, get_major_on_stat, get_int_from_fields)
    dict_[cmc.b_block_minor] = Metadata(cmc.b_block_minor, get_minor_on_stat, get_int_from_fields)
    dict_[cmc.b_character_device] = Metadata(cmc.b_character_device, always_true, get_bool_from_fields)
    dict_[cmc.b_character_major] = Metadata(cmc.b_character_major, get_major_on_stat, get_int_from_fields)
    dict_[cmc.b_character_minor] = Metadata(cmc.b_character_minor, get_minor_on_stat, get_int_from_fields)
    dict_[cmc.b_directory] = Metadata(cmc.b_directory, always_true, get_bool_from_fields)
    dict_[cmc.b_fifo] = Metadata(cmc.b_fifo, always_true, get_bool_from_fields)
    dict_[cmc.b_group] = Metadata(cmc.b_group, get_group_on_stat, get_escaped_string_from_fields)
    dict_[cmc.b_hash] = Metadata(cmc.b_hash, init_hashes_on_stat, get_hashes_from_fields)
    dict_[cmc.b_link_target] = Metadata(cmc.b_link_target, get_link_target_on_stat, get_escaped_string_from_fields)
    dict_[cmc.b_owner] = Metadata(cmc.b_owner, get_owner_on_stat, get_escaped_string_from_fields)
    dict_[cmc.b_regular_file] = Metadata(cmc.b_regular_file, always_true, get_bool_from_fields)
    dict_[cmc.b_symlink] = Metadata(cmc.b_symlink, always_true, get_bool_from_fields)
    dict_[cmc.b_st_atime] = Metadata(cmc.b_st_atime, get_field_on_stat, get_float_from_fields)
    dict_[cmc.b_st_ctime] = Metadata(cmc.b_st_ctime, get_field_on_stat, get_float_from_fields)
    dict_[cmc.b_st_dev] = Metadata(cmc.b_st_dev, get_field_on_stat, get_int_from_fields)
    dict_[cmc.b_st_gid] = Metadata(cmc.b_st_gid, get_field_on_stat, get_int_from_fields)
    dict_[cmc.b_st_ino] = Metadata(cmc.b_st_ino, get_field_on_stat, get_int_from_fields)
    dict_[cmc.b_st_mode] = Metadata(cmc.b_st_mode, get_field_on_stat, get_int_from_fields)
    dict_[cmc.b_st_mtime] = Metadata(cmc.b_st_mtime, get_field_on_stat, get_float_from_fields)
    dict_[cmc.b_st_size] = Metadata(cmc.b_st_size, get_field_on_stat, get_int_from_fields)
    dict_[cmc.b_st_uid] = Metadata(cmc.b_st_uid, get_field_on_stat, get_int_from_fields)


class File_types(object):
    # pylint: disable=W0232,R0903
    # W0232: This class doesn't need an __init__
    # R0903: We don't require public methods for this class
    """Just hold the different file types, their metadata fields, and how to convert each type of attribute."""

    cmc = constants_mod.Constants

    dict_ = {}
    dict_[cmc.b_directory] = [
        File_attributes.dict_[cmc.b_directory],
        File_attributes.dict_[cmc.b_group],
        File_attributes.dict_[cmc.b_owner],
        File_attributes.dict_[cmc.b_st_ctime],
        File_attributes.dict_[cmc.b_st_dev],
        File_attributes.dict_[cmc.b_st_gid],
        File_attributes.dict_[cmc.b_st_ino],
        File_attributes.dict_[cmc.b_st_mode],
        File_attributes.dict_[cmc.b_st_mtime],
        File_attributes.dict_[cmc.b_st_uid],
    ]
    dict_[cmc.b_regular_file] = [
        File_attributes.dict_[cmc.b_group],
        File_attributes.dict_[cmc.b_hash],
        File_attributes.dict_[cmc.b_owner],
        File_attributes.dict_[cmc.b_regular_file],
        File_attributes.dict_[cmc.b_st_ctime],
        File_attributes.dict_[cmc.b_st_dev],
        File_attributes.dict_[cmc.b_st_gid],
        File_attributes.dict_[cmc.b_st_ino],
        File_attributes.dict_[cmc.b_st_mode],
        File_attributes.dict_[cmc.b_st_mtime],
        File_attributes.dict_[cmc.b_st_size],
        File_attributes.dict_[cmc.b_st_uid],
    ]
    dict_[cmc.b_symlink] = [
        File_attributes.dict_[cmc.b_group],
        File_attributes.dict_[cmc.b_link_target],
        File_attributes.dict_[cmc.b_owner],
        File_attributes.dict_[cmc.b_st_ctime],
        File_attributes.dict_[cmc.b_st_gid],
        File_attributes.dict_[cmc.b_st_mode],
        File_attributes.dict_[cmc.b_st_mtime],
        File_attributes.dict_[cmc.b_st_uid],
        File_attributes.dict_[cmc.b_symlink],
    ]
    dict_[cmc.b_block_device] = [
        File_attributes.dict_[cmc.b_block_device],
        File_attributes.dict_[cmc.b_block_major],
        File_attributes.dict_[cmc.b_block_minor],
        File_attributes.dict_[cmc.b_group],
        File_attributes.dict_[cmc.b_owner],
        File_attributes.dict_[cmc.b_st_ctime],
        File_attributes.dict_[cmc.b_st_dev],
        File_attributes.dict_[cmc.b_st_gid],
        File_attributes.dict_[cmc.b_st_ino],
        File_attributes.dict_[cmc.b_st_mode],
        File_attributes.dict_[cmc.b_st_mtime],
        File_attributes.dict_[cmc.b_st_uid],
    ]
    dict_[cmc.b_character_device] = [
        File_attributes.dict_[cmc.b_character_device],
        File_attributes.dict_[cmc.b_character_major],
        File_attributes.dict_[cmc.b_character_minor],
        File_attributes.dict_[cmc.b_group],
        File_attributes.dict_[cmc.b_owner],
        File_attributes.dict_[cmc.b_st_ctime],
        File_attributes.dict_[cmc.b_st_dev],
        File_attributes.dict_[cmc.b_st_gid],
        File_attributes.dict_[cmc.b_st_ino],
        File_attributes.dict_[cmc.b_st_mode],
        File_attributes.dict_[cmc.b_st_mtime],
        File_attributes.dict_[cmc.b_st_uid],
    ]
    dict_[cmc.b_fifo] = [
        File_attributes.dict_[cmc.b_fifo],
        File_attributes.dict_[cmc.b_group],
        File_attributes.dict_[cmc.b_owner],
        File_attributes.dict_[cmc.b_st_ctime],
        File_attributes.dict_[cmc.b_st_dev],
        File_attributes.dict_[cmc.b_st_gid],
        File_attributes.dict_[cmc.b_st_ino],
        File_attributes.dict_[cmc.b_st_mode],
        File_attributes.dict_[cmc.b_st_mtime],
        File_attributes.dict_[cmc.b_st_uid],
    ]
