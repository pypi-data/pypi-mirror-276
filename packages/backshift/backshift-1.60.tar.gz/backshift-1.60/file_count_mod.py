#!/usr/bin/python3

"""Just hold the file count from progress modes - if any."""


class File_count(object):
    """Just a class to hold a file count from a progress mode, if any.  Some progress modes don't obtain one."""

    # pylint: disable=W0232,R0903
    # W0232: This class does not need an __init__ method
    # R0903: We don't need any public methods.  We're just a container
    file_count = None
