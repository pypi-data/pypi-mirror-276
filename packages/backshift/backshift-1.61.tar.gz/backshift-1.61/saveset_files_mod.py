#!/usr/bin/env python

"""A simple class for operating on the file list portion of a saveset."""

import errno
import functools
import os

import backshift_file_mod
import compressed_file_mod
import constants_mod
import db_mod
import dirops_mod
import helpers


def convert_filename(filename):
    """Convert a filename to a sort of normalized form: Make it "binary", and strip off the leading / (os.path.sep)."""
    bytes_filename = helpers.string_to_binary(filename)
    bytes_path_sep = helpers.string_to_binary(os.path.sep)
    stripped_filename = bytes_filename.lstrip(bytes_path_sep)
    return stripped_filename


def prepend_dir_prefix(path, start_from=0):
    """Prepend dir- prefixes."""
    # FIXME: Can this becomes just a path.split on 3.x-only?
    if isinstance(path, bytes):
        path_components = path.split(helpers.string_to_binary(os.path.sep))
    else:
        path_components = path

    prefix = constants_mod.Constants.b_dir_dash
    prefixed_path_components = []
    for dirno, directory in enumerate(path_components):
        if dirno >= start_from:
            prefixed_path_components.append(prefix + directory)
        else:
            prefixed_path_components.append(directory)

    bytes_path_sep = helpers.string_to_binary(os.path.sep)

    rejoined = bytes_path_sep.join(prefixed_path_components)

    return rejoined


class Saveset_files(object):
    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods.  At least, not yet.
    """A simple class for operating on the file list portion of a saveset."""

    def __init__(self, repo, saveset_summary=None):
        """Initialize."""
        self.repo = repo

        if saveset_summary is None:
            backup_id = repo.backup_id
        else:
            backup_id = saveset_summary.backup_id
        self.backup_id = helpers.string_to_binary(backup_id)

        files = constants_mod.Constants.b_files
        self.early_dirs = os.path.join(files, self.backup_id)

    def _get_database_and_basename(self, filename, mode):
        """Look up the database and key corresponding to filename, if any."""
        converted_filename = convert_filename(filename)
        filename_plus_early_dirs = os.path.join(self.early_dirs, converted_filename)
        directory = os.path.dirname(filename_plus_early_dirs)
        prefixed_directory = prepend_dir_prefix(directory, start_from=2)

        bytes_entries = constants_mod.Constants.b_entries
        entries_path = os.path.join(prefixed_directory, bytes_entries)
        basename = os.path.basename(converted_filename)

        if directory in self.repo.database_cache:
            database = self.repo.database_cache[directory]
        else:
            # we only need to create the directory if the database isn't in the cache - actually, less than that,
            # but this heuristic helps
            dirops_mod.my_mkdir(prefixed_directory)
            # This is our primary deviation from standard *dbm files: We save data compressed.
            # Drop the backend_open argument, and we have regular, uncompressed output for metadata,
            # suitable for use with gdbm or similar.  See also where these are read, in repo_mod.py.
            backend_open = functools.partial(compressed_file_mod.Compressed_file, start_empty=True, zero_length_ok=True)
            database = db_mod.open(entries_path, mode, backend_open=backend_open)
            self.repo.database_cache[directory] = database

        return database, basename

    def put_filename(self, filename, backshift_file):
        """
        Write one Backshift_file to a database containing file metadata.

        Includes hashes and lengths of chunks where appropriate.
        """
        database, basename = self._get_database_and_basename(filename, 'wb')
        database[basename] = backshift_file.as_string()

    def get_filename(self, filename):
        """Read one file back from its containing directory, returning it as a Backshift_file."""
        try:
            database, basename = self._get_database_and_basename(filename, 'rb')
        except (OSError, IOError) as extra:
            if extra.errno == errno.ENOENT:
                return None
            else:
                raise
        if basename in database:
            return backshift_file_mod.Backshift_file(self.repo, database[basename], filename)
        return None
