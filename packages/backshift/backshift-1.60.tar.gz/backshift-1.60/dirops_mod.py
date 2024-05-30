
"""Module of one function: my_mkdir,which creates directories as needed."""

import os
import re
import errno

import constants_mod
import helpers


class ExistingDirs(object):
    """Keep track of directories seen recently, that we know (pre)exist."""

    def __init__(self):
        """Initialize."""
        self.dirs = []
        self.count = 0
        self.limit_list = 100

    def add(self, path):
        """Add path to list of dirs, keeping only the last self.limit_list entries."""
        if path in self.dirs:
            self.dirs.remove(path)
        self.dirs.append(path)
        self.count = self.count + 1
        if self.count >= self.limit_list:
            self.dirs = self.dirs[-self.limit_list:]

    def exists(self, path):
        """Test if a path is known to exist."""
        result = path in self.dirs
        return result


EXISTINGDIRS = ExistingDirs()


def my_mkdir(pathname):
    """
    Create one or more directories specified by directory_list.

    If pathname has [ 'a', 'b', 'c' ], then we create a/b/c.
    If pathname has 'a/b/c' then we create a/b/c
    """
    bytes_path_sep = helpers.string_to_binary(os.path.sep)

    if isinstance(pathname, str):
        complete_relative_path = helpers.string_to_binary(pathname)
        directory_list = helpers.string_to_binary(pathname).split(bytes_path_sep)
    elif isinstance(pathname, bytes):
        # Sometimes this'll be str - handled above
        complete_relative_path = pathname
        directory_list = pathname.split(bytes_path_sep)
    elif isinstance(pathname, list):
        complete_relative_path = os.path.join(*pathname)
        directory_list = pathname
    else:
        raise ValueError('pathname is not str, bytes or list')

    if EXISTINGDIRS.exists(complete_relative_path):
        return
    if os.path.isdir(complete_relative_path):
        EXISTINGDIRS.add(complete_relative_path)
        return

    for final_position in range(1, len(directory_list) + 1):
        partial_relative_slice = directory_list[:final_position]
        partial_relative_path = os.path.join(*partial_relative_slice)
        if EXISTINGDIRS.exists(partial_relative_path):
            continue
        try:
            os.mkdir(partial_relative_path, 7 * 64 + 5 * 8 + 5)
            EXISTINGDIRS.add(partial_relative_path)
        except OSError as mkdir_extra:
            if mkdir_extra.errno == errno.EEXIST:
                EXISTINGDIRS.add(partial_relative_path)
                continue
            else:
                raise


def prepend_dirs(path):
    """Take a relative path and add dir- prefixes to all the directories."""
    path_parts, filename = get_path_parts(path)
    directories = path_parts[:]
    # filename is a directory too in this case
    directories.append(filename)
    nonempty_directories = [directory for directory in directories if directory and directory != constants_mod.Constants.b_dot]
    dired_directories = ['dir-%s' % helpers.binary_to_string(directory) for directory in nonempty_directories]
    if not dired_directories:
        dired_directories = ['.']
    result = os.path.join(*dired_directories)
    return result


def strip_dirs(pathname):
    """Strip off all the dir- prefixes."""
    path1 = re.sub(constants_mod.Constants.b_slash_dir_dash, constants_mod.Constants.b_slash, helpers.string_to_binary(pathname))
    path2 = re.sub(constants_mod.Constants.b_hat_dot_slash, helpers.empty_bytes, path1)
    path3 = re.sub(constants_mod.Constants.b_hat_dir_dash, helpers.empty_bytes, path2)
    return path3


def get_path_parts(relative_path):
    """Chop a (directory-containing) pathname into the directory leading up to it (dirname), and its final part (basename)."""
    if isinstance(relative_path, list):
        path_components = relative_path
    else:
        bin_rel_path = helpers.string_to_binary(relative_path)
        bin_sep = helpers.string_to_binary(os.path.sep)
        path_components = bin_rel_path.split(bin_sep)
    nonempty_path_components = [component for component in path_components if component != helpers.empty_bytes]
    relative_directories = nonempty_path_components[:-1]
    if nonempty_path_components:
        filename = nonempty_path_components[-1]
    else:
        filename = helpers.string_to_binary(os.path.sep)

    return (relative_directories, filename)
