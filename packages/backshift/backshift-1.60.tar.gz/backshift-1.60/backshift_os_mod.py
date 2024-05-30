
"""This module is to handle miscellaneous, OS-related callables."""

import os
import grp
import pwd
import sys
import errno


def safe_rename(backup_filename, regular_filename):
    """Rename backup_filename to regular_filename."""
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


class memoize(object):
    # pylint: disable=R0903
    # R0903: We have a very focused purpose, and don't require a lot of public methods
    """Cache a function's results."""

    # Shamelessly lifted from http://www.quora.com/Is-there-a-decorator-that-does-memoization-built-in-to-Python
    def __init__(self, function):
        """Initialize."""
        self.function = function
        self.memoized = {}

    def __call__(self, *args):
        """Make us callable, like a decorator."""
        try:
            return self.memoized[args]
        except KeyError:
            self.memoized[args] = self.function(*args)
            return self.memoized[args]


@memoize
def my_getpwnam(name):
    """Look up a pwent by username - cached."""
    return pwd.getpwnam(name)


@memoize
def my_getpwuid(uid):
    """Look up a pwent by userid - cached."""
    return pwd.getpwuid(uid)


@memoize
def my_getgrnam(name):
    """Look up a grent by group name - cached."""
    return grp.getgrnam(name)


@memoize
def my_getgrgid(gid):
    """Look up a grent by groupid - cached."""
    return grp.getgrgid(gid)
