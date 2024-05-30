#!/usr/bin/env python3

"""Provides a bunch of str/bytes constants, so we aren't converting and reconverting incessantly."""


class Constants(object):
    # pylint: disable=W0232,R0903
    # W0232: We don't need an __init__ for a container
    # R0903: We don't need public methods for a container
    """Just a simple container for lots of things we need as bytes."""

    # First some file metadata attributes
    b_block_device = b'block_device'
    b_block_major = b'block_major'
    b_block_minor = b'block_minor'
    b_character_device = b'character_device'
    b_character_major = b'character_major'
    b_character_minor = b'character_minor'
    b_directory = b'directory'
    b_fifo = b'fifo'
    b_group = b'group'
    b_hardlink = b'hardlink'
    b_hash = b'hash'
    b_link_target = b'link_target'
    b_owner = b'owner'
    b_regular_file = b'regular_file'
    b_st_atime = b'st_atime'
    b_st_ctime = b'st_ctime'
    b_st_dev = b'st_dev'
    b_st_gid = b'st_gid'
    b_st_ino = b'st_ino'
    b_st_mode = b'st_mode'
    b_st_mtime = b'st_mtime'
    b_st_size = b'st_size'
    b_st_uid = b'st_uid'
    b_symlink = b'symlink'
    b_readlink_failed = b'readlink failed'

    # Some single character things for string manipulation
    b_newline = b'\n'
    b_cr = b'\r'
    b_tab = b'\t'
    b_question = b'?'
    b_blank = b' '
    b_minus = b'-'

    # Some directory-related constants
    b_dot = b'.'
    b_slash_dir_dash = b'/dir-'
    b_slash = b'/'
    b_hat_dot_slash = br'^\./'
    b_hat_dir_dash = b'^dir-'
    b_dir_dash = b'dir-'

    # Some file extensions
    b_dot_data = b'.data'
    b_dot_time = b'.time'

    # Some file/directory commponents
    b_chunks = b'chunks'
    b_files = b'files'
    s_entries = 'entries'
    b_entries = b'entries'
    b_data = b'data'
    b_time = b'time'

    # Some miscellaneous constants
    b_true = b'True'
    b_false = b'False'
    file_type_width = 7

    # Some characters for grouping
    b_a = b'a'
    b_z = b'z'
    b_A = b'A'
    b_Z = b'Z'
    b_0 = b'0'
    b_1 = b'1'
    b_2 = b'2'
    b_3 = b'3'
    b_4 = b'4'
    b_5 = b'5'
    b_6 = b'6'
    b_7 = b'7'
    b_8 = b'8'
    b_9 = b'9'
    b_underscore = b'_'
    b_special = b'`~!@#$%^&*()-_=+[{]}\\|;:",<.>/?' + b"'"
    b_onenewline = b'1\n'

    block_size = 2 ** 18
