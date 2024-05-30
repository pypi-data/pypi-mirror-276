
# pylint: disable=superfluous-parens

"""
Functions related to expiring old data from a repo.

Sort of belongs in repo_mod, but doesn't really have much overlap, and repo_mod is getting kind of big.
"""

import decimal
import glob
import os
import re
import shutil
import sys
import time

import chunk_mod
import dirops_mod
import helpers
import repo_mod
import saveset_summary_mod
import xz_mod


def make_used(*var):
    """Persuade linters that var is used."""
    assert True or var


def expire(current_time, check_hashes):
    """Expire old chunks, files and savesets from this repository."""
    # Please note that we decide whether something is a hash based on directory+file lengths.  We don't (yet?) attempt to
    # confirm that a directory+file is lower case hexadecimal or anything like that.

    our_directory = 'overall'

    dirops_mod.my_mkdir(our_directory)

    maximum_age = get_maximum_age(our_directory)

    expire_savesets(current_time, maximum_age)
    expire_files(current_time, maximum_age)
    expire_hashes(current_time, maximum_age, check_hashes)


def get_maximum_age(our_directory):
    """Get the maximum age for the repo, one way or another."""
    our_filename = os.path.join(our_directory, 'maximum-age')

    try:
        file_ = open(our_filename, 'r')
    except (OSError, IOError):
        # We don't appear to have a maximum-age file yet - ask the user for a time, and create one
        sys.stderr.write('This appears to be the first time you have used --expire;\n')
        sys.stderr.write('Please enter the maximum age of files in seconds.\n')
        sys.stderr.write('For a 365 day year, compute 60*60*24*365 == 31536000 and enter 31536000.\n')
        sys.stderr.write('To account for leap years, etcetera, you can use 60*60*24*365.2421891 == 31556925.\n')
        sys.stderr.write('> ')
        line = sys.stdin.readline()
        maximum_age = float(line)
        file_ = open(our_filename, 'w')
        file_.write('%f\n' % maximum_age)
        file_.close()
    else:
        # Reuse a previous maximum-age file
        line = file_.readline()
        maximum_age = float(line)

    return maximum_age


def expire_hashes(current_time, maximum_age, check_hashes):
    """Expire all old hashes.  Build a list of current hashes."""
    sys.stderr.write('Removing old chunks\n')

    sample_hash = repo_mod.get_hash(helpers.null_byte)

    hash_len = len(sample_hash)

    chunks_string = 'chunks'

    chunks_expiration_traversal(current_time, maximum_age, chunks_string, hash_len, check_hashes)


def expire_files(current_time, maximum_age):
    """Expire all old hashes.  Build a list of current hashes."""
    current_time = time.time()

    files_string = 'files'

    files_expiration(current_time, maximum_age, files_string)


def rmtree_onerror(function, path, exception):
    """Deal with errors from rmtree."""
    make_used(function, exception)

    sys.stderr.write('{}: {} failed to unlink\n'.format(sys.argv[0], path))


def files_expiration(current_time, maximum_age, files_string):
    """Recursively remove files directories that are now too old."""
    for dirname in glob.glob('%s/*' % files_string):
        dirtime = os.stat(dirname).st_mtime

        if current_time - dirtime > maximum_age:
            sys.stdout.write('Removing files hierarchy %s\n' % dirname)
            shutil.rmtree(dirname, onerror=rmtree_onerror)


def is_empty_dir(prefix, list_of_subdirs, list_of_filenames, hash_len):
    """
    Return True iff directory is empty.

    prefix is the hexadecial derived from this directory.
    list_of_subdirs is a (possibly empty) list of subdirectories of this directory.
    list_of_filenames is a (possibly empty) list of filenames in this directory.
    hash_len is the length we expect a good hash to have.
    """
    # sys.stderr.write('checking directory %s\n' % (directory, ))
    if list_of_subdirs:
        # We have subdirectories, so this is not empty
        return False

    # This gives us a list of filenames which are hashes. It intentionally excludes temporary filenames as
    # created by chunk_mod_traditional.py
    # We could improve it a bit by checking for temporary files that are recent/old.  But there would still be a race condition.
    hash_filenames = []
    for filename in list_of_filenames:
        # Note that it's possible for full_hash to not be an actual hash! EG if someone stashed a README in a chunk directory.
        full_hash = prefix + filename
        # temp files have underscores in them, until they are renamed.
        if len(full_hash) == hash_len and '_' not in filename:
            hash_filenames.append(filename)

    if hash_filenames:
        # we have at least one hash_filename, so this directory is not 'empty'
        return False

    return True


def is_old_dir(directory, high_age):
    """Return True iff directory is old."""
    current_time = time.time()
    directory_time = os.path.getmtime(directory)
    age = current_time - directory_time
    return age >= high_age


# high_age is about 2 months.
def chunks_expiration_traversal(current_time, maximum_age, chunks_string, hash_len, check_hashes):
    # pylint: disable=too-many-locals
    """Traverse the chunks tree, deleting old files and optionally verifying hashes as we go."""
    # The followlinks option to os.walk wasn't introduced until Python 2.6, and we support Python 2.5, including
    # early PyPy, and Jython.
    previous_hex = ''
    high_age = 60 * 60 * 24 * 30 * 2
    directories_deleted = 0
    hashes_deleted = 0
    for internal_root_dir, list_of_dirs, list_of_filenames in os.walk(chunks_string, topdown=True):
        # We want this to make os.walk give us back directories in sorted order - to maximize the benefit of our in-filesystem trie
        # datastructure.
        list_of_dirs.sort()

        fields = internal_root_dir.split(os.sep)

        if len(fields) == 2:
            assert fields[0] == chunks_string
            current_hex = fields[1][:2]
            if current_hex != previous_hex:
                print('0x{} of 0x100 ({} hashes deleted, {} directories deleted)'.format(
                    current_hex,
                    hashes_deleted,
                    directories_deleted
                ))
                previous_hex = current_hex

        prefix = internal_root_dir
        for regex in [re.compile('^%s%s' % (chunks_string, os.path.sep)), re.compile(os.path.sep)]:
            prefix = re.sub(regex, '', prefix)

        # Is this an old, 'empty' directory?
        if is_empty_dir(
                prefix,
                list_of_dirs,
                list_of_filenames,
                hash_len) and is_old_dir(internal_root_dir, high_age):
            # Yes, so remove it. We use rmtree because directories containing nothing but temporaries are considered
            # 'empty'.
            # sys.stderr.write('removing %s\n' % (internal_root_dir, ))
            shutil.rmtree(internal_root_dir)
            directories_deleted += 1
            continue

        for filename in list_of_filenames:
            full_hash = prefix + filename
            full_path = os.path.join(internal_root_dir, filename)

            if len(full_hash) == hash_len:
                if expire_one_hash(current_time, maximum_age, full_path, full_hash, check_hashes):
                    hashes_deleted += 1


def expire_one_hash(current_time, maximum_age, full_path, full_hash, check_hashes):
    """Expire one hash file."""
    deleted = False
    statbuf = os.stat(full_path)
    if statbuf.st_mtime < current_time - maximum_age:
        # Chunk file is too old - remove it
        os.unlink(full_path)
        deleted = True
    elif statbuf.st_size == 0:
        # Most commonly, if a filesystem gets corrupted, that'll manifest as zero-length files
        os.unlink(full_path)
        deleted = True
        sys.stderr.write('%s: unlinked zero-length (corrupted) hash file %s.\n' % (sys.argv[0], full_path))
        sys.stderr.write('Next time you back up a file with this hash, it will be recreated.\n')
    elif check_hashes:
        chunk = chunk_mod.Chunk(full_hash)
        try:
            data = chunk.read_chunk()
        except OSError:
            sys.stderr.write('%s: Got an OSError (disk, filesystem) reading %s .\n' % (sys.argv[0], full_path))
            sys.stderr.write('You could try removing the file and attempting again, but this likely means disk or\n')
            sys.stderr.write('filesystem corruption!\n')
            sys.exit(1)
        except xz_mod.DecompressionError:
            # Note that we've checked for decompression problems in chunks, but not in metadata.  Doing the
            # same for metadata would be good too.
            sys.stderr.write('%s: Warning: Chunk that failed to decompress; unlinking: %s\n' % (sys.argv[0], full_path))
            deleted = True
            os.unlink(full_path)
        else:
            if repo_mod.get_hash(data) != full_hash:
                sys.stderr.write('%s: Warning: Chunk found with bad digest; unlinking: %s\n' % (sys.argv[0], full_path))
                deleted = True
                os.unlink(full_path)

    return deleted


def expire_savesets(current_time, maximum_age):
    """Expire old savesets."""
    # canonical_hostname is unused when backup_id is None.
    # We've already cd'd - no need to pass anything special into save_directory.
    saveset_summaries = saveset_summary_mod.get_all_saveset_summaries(save_directory='.', canonical_hostname='')

    for saveset_summary in saveset_summaries:
        # It's kind of important that we use finish_time here and not start_time.  Otherwise, we could end up expiring
        # a saveset corresponding to partially-expired chunks, because sometimes saves take a while.
        youngest_to_keep = decimal.Decimal(str(current_time - maximum_age))

        saveset_summary_path = os.path.join(saveset_summary_mod.SUMMARIES_NAME, saveset_summary.backup_id)

        # Sometimes a save terminates early without a finish_time recorded; we cope with that by using the summary mtime instead
        finish_time = saveset_summary.finish_time
        if finish_time is None:
            statbuf = os.stat(saveset_summary_path)
            finish_time = decimal.Decimal(str(statbuf.st_mtime))
        else:
            finish_time = decimal.Decimal(finish_time)

        if finish_time < youngest_to_keep:
            sys.stdout.write('Unlinking saveset summary %s with finish_time %s (%s)\n' % (
                saveset_summary.backup_id,
                saveset_summary.finish_time,
                'None' if finish_time is None else time.ctime(float(finish_time)),
            ))
            os.unlink(saveset_summary_path)
