
"""Provides a backup repository class."""

from __future__ import print_function

import collections
import errno
import hashlib  # pylint: disable=F0401
import os
import platform
import stat
import sys
import tarfile
import time

import backshift_file_mod
import bufsock
import cacher_mod
import chunk_mod
import compressed_file_mod
import constants_mod
import db_mod
import dirops_mod
import file_count_mod
import hardlinks_mod
import helpers
import rolling_checksum_mod
import saveset_files_mod
import saveset_summary_mod
import xz_mod


VALID_TAR_FORMATS = {
    'default': tarfile.DEFAULT_FORMAT,
    'ustar': tarfile.USTAR_FORMAT,
    'gnu': tarfile.GNU_FORMAT,
    'pax': tarfile.PAX_FORMAT,
}


def make_used(var):
    """Persuade pyflakes that var is used."""
    assert True or var


def get_hash(chunk):
    # pylint: disable=E1101
    # E1101: Actually, hashlib does have a sha256 member.  Please don't complain about nonsense, pylint.
    """Get the hash of this chunk, and create a relative path from it."""
    hasher = hashlib.sha256(chunk)
    digest = hasher.hexdigest()

    return digest


class Games_detected(Exception):
    """An exception to raise when some pranks have been detected (or some kinds of changes during the backup)."""

    pass


class Permission_denied(Exception):
    """An exception to raise when a file can't be opened due to EPERM."""

    pass


class Missing_chunk(Exception):
    """An exception to raise when a one (or more) of the chunks in an st_mtime+st_size match are missing."""

    # Sometimes filesystems have problems.  Specifically, sometimes files that should have data, come up with st_size 0 in
    # the event of a system crash or similar.  We want the user to be able to just delete such files and get them saved
    # correctly next time that chunk is to be saved.
    pass


# pylint: disable=W0603
# W0603: We really do kinda need something with a global lifetime here
if hasattr(os, 'fstat'):
    HAVE_FSTAT = True
else:
    HAVE_FSTAT = False
    FSTAT_ANNOUNCED = False


def no_games(lstat_result, file_handle):
    """
    Make sure no games are being played with the file to exploit a race window.

    We might also be tripped by legimate changes if they happen at just the "right" moment...
    """
    global FSTAT_ANNOUNCED

    # FIXME: This might actually be erring too much on the safe side.
    if HAVE_FSTAT:
        try:
            fstat_result = os.fstat(file_handle.fileno())
        except OSError as fstat_extra:
            if fstat_extra.errno == errno.ENOENT:
                raise Games_detected('File disappeared during race window.')
            else:
                raise
        if lstat_result.st_ino != fstat_result.st_ino or lstat_result.st_dev != fstat_result.st_dev:
            raise Games_detected('Inode and/or device file number(s) changed')
        if lstat_result.st_uid != fstat_result.st_uid or lstat_result.st_gid != fstat_result.st_gid:
            raise Games_detected('uid and/or gid number(s) changed')
        if lstat_result.st_mode != fstat_result.st_mode:
            raise Games_detected('File mode changed')
        if stat.S_ISREG(fstat_result.st_mode):
            return
        else:
            raise Games_detected('No longer a regular file')
    else:
        if not FSTAT_ANNOUNCED:
            sys.stderr.write('%s: Warning: This Python has no fstat with which to detect symlink races\n' % sys.argv[0])
            FSTAT_ANNOUNCED = True
        return


def display_tvf(backshift_file, hardlink_data):
    """Display a "tar tvf"-like listing for a specific file."""
    bytes_data = helpers.string_to_binary(backshift_file.to_tar_tvf(hardlink_data))
    os.write(1, b'%b\n' % bytes_data)


def display_tf(backshift_file, hardlink_data):
    """Display a "tar tf"-like listing for a specific file."""
    make_used(hardlink_data)
    bytes_data = helpers.string_to_binary(backshift_file.to_tar_tf())
    os.write(1, b'%b\n' % bytes_data)


class File_like_empty(object):
    # pylint: disable=R0903
    # R0903: We don't need many public methods
    """A file like object that pretends to be an empty file."""

    def __init__(self):
        """Initialize the 'empty file'."""
        pass

    def read(self, length):
        # pylint: disable=R0201
        # R0201: We can't really be a function, because we have to accept a length
        """Act like we're at EOF - always."""
        make_used(length)
        return helpers.empty_bytes


class File_like_pieces(object):
    # pylint: disable=R0903
    # R0903: We don't need many public methods
    """A file-like object that slurps in chunks from our content directory."""

    def __init__(self, hashes):
        """
        Initialize 'the file'.

        chunk_description will be a list of tuples - tuple_[0] is the hash, tuple_[1] is the length of the chunk.
        """
        self.chunk_description = hashes
        self.total_length = sum(chunk[1] for chunk in self.chunk_description)
        self.on_chunk = 0
        self.num_chunks = len(self.chunk_description)
        self.position = 0
        self.currently_have = helpers.empty_bytes

    def read(self, length_desired):
        """Read length_desired bytes from 'the file'."""
        while len(self.currently_have) < length_desired:
            chunk_length = self.chunk_description[self.on_chunk][1]
            if self.position + chunk_length > self.total_length:
                chunk_length = self.total_length - self.position
            if chunk_length == 0:
                # we've inhaled all we're gonna (supposed to) get already
                break
            if self.on_chunk > self.num_chunks:
                # This should never happen, because we already checked if we're at EOF via the if chunk_length == 0 above
                raise AssertionError('self.on_chunk > self.num_chunks')
            digest = self.chunk_description[self.on_chunk][0]
            chunk = chunk_mod.Chunk(digest)
            try:
                new_chars = chunk.read_chunk()
            except xz_mod.DecompressionError:
                # Note that we've checked for decompression problems in chunks, but not in metadata.  Doing the
                # same for metadata would be good too.
                sys.stderr.write('%s: decompression error on chunk %s\n' % (sys.argv[0], digest))
                sys.stderr.write('This is likely due to disk errors or filesystem corruption. Replacing with nulls in output\n')
                new_chars = b'\0' * chunk_length
            self.on_chunk += 1
            if len(new_chars) != chunk_length:
                raise AssertionError('len(new_chars); %d, chunk_length: %d, digest: %s' % (len(new_chars), chunk_length, digest))
            self.currently_have += new_chars
        # advance the "file" pointer and dole out
        result = self.currently_have[:length_desired]
        self.currently_have = self.currently_have[length_desired:]
        return result


class Tar_state(object):
    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods; we're just a container
    """Save some state for our --produce-tar tree traversal."""

    def __init__(self, tar, hardlink_data):
        """Initialize."""
        self.tar = tar
        self.hardlink_data = hardlink_data


def give_tar(backshift_file, tar_state):
    """Produce a tar-format file entry for a specific file."""
    tarinfo = tarfile.TarInfo(name=helpers.binary_to_string(backshift_file.filename))

    tarinfo.mtime = backshift_file.dict_[constants_mod.Constants.b_st_mtime]
    tarinfo.uname = helpers.binary_to_string(backshift_file.dict_[constants_mod.Constants.b_owner])
    tarinfo.gname = helpers.binary_to_string(backshift_file.dict_[constants_mod.Constants.b_group])
    tarinfo.uid = backshift_file.dict_[constants_mod.Constants.b_st_uid]
    tarinfo.gid = backshift_file.dict_[constants_mod.Constants.b_st_gid]
    tarinfo.mode = backshift_file.dict_[constants_mod.Constants.b_st_mode]
    # REGTYPE, AREGTYPE, LNKTYPE, SYMTYPE, DIRTYPE, FIFOTYPE, CONTTYPE, CHRTYPE, BLKTYPE, GNUTYPE_SPARSE
    if backshift_file.dict_.get(constants_mod.Constants.b_regular_file):
        deviceno = backshift_file.dict_[constants_mod.Constants.b_st_dev]
        inodeno = backshift_file.dict_[constants_mod.Constants.b_st_ino]
        current_filename = backshift_file.filename
        prior_filename = tar_state.hardlink_data.prior_file_for_hardlink(deviceno, inodeno, current_filename)
        if prior_filename:
            # This is a hardlink - treat it as such
            tarinfo.type = tarfile.LNKTYPE
            tarinfo.linkname = helpers.binary_to_string(prior_filename)
            tar_state.tar.addfile(tarinfo)
        else:
            # This is either not a hardlinked file, or the first file of 2 or more hardlinked files - make it distinct
            tarinfo.type = tarfile.REGTYPE
            hashes = backshift_file.dict_.get(constants_mod.Constants.b_hash)
            if hashes is None:
                tarinfo.size = 0
                tar_state.tar.addfile(tarinfo, File_like_empty())
            else:
                flp = File_like_pieces(hashes)
                tarinfo.size = flp.total_length
                tar_state.tar.addfile(tarinfo, flp)
    elif backshift_file.dict_.get(constants_mod.Constants.b_directory):
        tarinfo.type = tarfile.DIRTYPE
        tar_state.tar.addfile(tarinfo)
    elif backshift_file.dict_.get(constants_mod.Constants.b_symlink):
        tarinfo.type = tarfile.SYMTYPE
        tarinfo.linkname = helpers.binary_to_string(backshift_file.dict_[constants_mod.Constants.b_link_target])
        tar_state.tar.addfile(tarinfo)
    elif backshift_file.dict_.get(constants_mod.Constants.b_fifo):
        tarinfo.type = tarfile.FIFOTYPE
        tar_state.tar.addfile(tarinfo)
    elif backshift_file.dict_.get(constants_mod.Constants.b_character_device):
        tarinfo.type = tarfile.CHRTYPE
        tarinfo.devmajor = backshift_file.dict_[constants_mod.Constants.b_character_major]
        tarinfo.devminor = backshift_file.dict_[constants_mod.Constants.b_character_minor]
        tar_state.tar.addfile(tarinfo)
    elif backshift_file.dict_.get(constants_mod.Constants.b_block_device):
        tarinfo.type = tarfile.BLKTYPE
        tarinfo.devmajor = backshift_file.dict_[constants_mod.Constants.b_block_major]
        tarinfo.devminor = backshift_file.dict_[constants_mod.Constants.b_block_minor]
        tar_state.tar.addfile(tarinfo)
    else:
        sys.stderr.write('%s: Unrecognized file type: %s\n' % (sys.argv[0], backshift_file.filename))
        return


def format_time(num_seconds):
    """Convert a number of seconds since the epoch to a human readable string."""
    if num_seconds is None:
        return None
    return time.ctime(float(num_seconds)).replace(' ', '-')


def borrow_and_save_chunks(dict_, prior_backshift_file):
    """
    Save the chunks of a file by copying them from a previous backup d hashing them - fast.

    If one or more of the chunks doesn't exist, raise Missing_chunk.
    """
    # Sharing a reference here is probably fine, but it makes me a little squeamish, so we create a new list

    dict_[constants_mod.Constants.b_hash] = []
    for record in prior_backshift_file.dict_[constants_mod.Constants.b_hash]:
        digest, length = record
        helpers.make_used(length)
        dict_[constants_mod.Constants.b_hash].append(record)
        chunk = chunk_mod.Chunk(digest)
        try:
            chunk.update_timestamp()
        except (OSError, IOError) as update_timestamp_extra:
            if update_timestamp_extra.errno == errno.ENOENT:
                raise Missing_chunk
            else:
                raise


def save_chunk_at_hash(chunk_bytes):
    """Save a chunk under its hash.  Return its sha256 digest."""
    digest = get_hash(chunk_bytes)

    chunk = chunk_mod.Chunk(digest)

    length_written = chunk.write_or_touch_chunk(chunk_bytes)

    return digest, length_written


def generate_and_save_chunks(lstat_result, filename, dict_):
    """Save the chunks of a file by generating variable-length blocks and hashing them - slow."""
    try:
        data_file = bufsock.bufsock(bufsock.rawio(filename, 'rb'), chunk_len=constants_mod.Constants.block_size)
    except (OSError, IOError) as open_extra:
        if open_extra.errno in [errno.EPERM, errno.EACCES, errno.ENOENT]:
            raise Permission_denied('Permission denied or file not found reading %s\n' % filename)
        else:
            raise

    try:
        no_games(lstat_result, data_file)
    except Games_detected as description:
        sys.stderr.write('Skipping %s: %s\n' % (filename, description))
        return 'skip'

    total_written = 0
    total_processed = 0
    for chunk in rolling_checksum_mod.min_max_chunker(data_file):
        len_chunk = len(chunk)
        digest, length_written = save_chunk_at_hash(chunk)
        dict_[constants_mod.Constants.b_hash].append('%s %s\n' % (digest, len_chunk))
        total_written += length_written
        total_processed += len_chunk
    # If actual_length != the lstat length, the file changed while we were backing it up.  If the file changed while we
    # were backing it up, the lengths might be different, or they might not.
    # dict_['actual_length'] = length

    data_file.close()

    if total_processed == 0:
        # to avoid division by zero - we've "done" 100% of a zero-length file
        percentage = 100
    else:
        percentage = total_written * 100.0 / total_processed
    percentile = int(percentage / 10) * 10

    return 'perc%03d' % percentile


class Speeds(object):
    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods
    """Maintain counts of the various kinds of speeds (per file)."""

    def __init__(self):
        """Initialize."""
        self.dict_ = collections.defaultdict(int)

    def add_speed(self, speed):
        """Increment the kind of this kind of speed."""
        self.dict_[speed] += 1

    def __str__(self):
        """Convert to str."""
        keys = list(self.dict_.keys())
        keys.sort()
        list_ = []
        for key in keys:
            list_.append('%*s: %d' % (constants_mod.Constants.file_type_width, key, self.dict_[key]))
        return '\n'.join(list_)


def pick_file_count_estimate(prior_saveset_summaries, least_value, actual_number):
    """
    Pick a reasonable estimate for the file count of this save in one of 3 ways.

    1) If we're using a progress mode that gets a file count (passed here in actual_number), use that.
    2) If we have one or more saves we're backing up relative to, get the largest file count from them, and double it
    3) Otherwise, use 10,000,000.  This should cover most filesystems today (2012-04-28), and uses only a modest amount of memory.
    """
    if actual_number is None:
        max_prior_file_count = None
        for save_summary in prior_saveset_summaries:
            if max_prior_file_count is None or save_summary.number_of_files > max_prior_file_count:
                max_prior_file_count = save_summary.number_of_files

        if max_prior_file_count is None:
            return least_value

        doubled_max_prior_file_count = 2 * max_prior_file_count

        if doubled_max_prior_file_count < least_value:
            result = least_value
        else:
            result = doubled_max_prior_file_count
        accuracy = ' estimate'
    else:
        result = actual_number
        accuracy = ''

    sys.stderr.write('Using file count%s of %d\n' % (accuracy, result))

    return result


def get_initial_directory(backup_id, directory, shorten):
    """Construct and return a repo-internal path to backup_id and directory."""
    if directory in (b'/', b'.', b'') and shorten:
        initial_directory = os.path.join('files', backup_id)
    else:
        initial_directory = os.path.join('files', backup_id, dirops_mod.prepend_dirs(directory))
    return initial_directory


class Repo(object):
    """A repo that holds saves and file metadata (including hashes) and chunks of files."""

    # pylint: disable=R0902,R0903
    # R0902: We need a bunch of instance constants_mod.Constants
    def __init__(self, save_directory, canonical_hostname, subset):
        """Initialize."""
        self.database_cache = None

        self.cd_count = 0

        self.speeds = Speeds()

        self.start_time = None
        self.backup_id = None

        self.reading = False
        self.writing = False

        self.canonical_hostname = canonical_hostname

        # Stash this for Chunk_mod.Chunk to use
        chunk_mod.Chunk.canonical_hostname = canonical_hostname

        self.subset = subset

        # We intentionally don't save save_directory; it's often relative

        self.save_directory = save_directory

        absolute_save_directory = os.path.abspath(save_directory)

        # We want this to be the sole chdir, to keep things simple and consistent
        os.chdir(absolute_save_directory)

        self.current_saveset_summary = None
        self.current_saveset_files = None

        self.prior_saveset_summaries = []
        self.prior_saveset_files = []

        self.files_saved = 0

        self.hardlinks = None

    def set_up_paths2(self):
        """Set up some more useful path attributes."""
        if self.writing:
            self.prior_saveset_summaries = saveset_summary_mod.pick_saveset_summaries(
                self.save_directory,
                self.canonical_hostname,
                self.subset,
                self.current_saveset_summary,
            )

            self.prior_saveset_summaries.sort()
            self.prior_saveset_summaries.reverse()

            self.prior_saveset_files = [saveset_files_mod.Saveset_files(self, summary) for summary in self.prior_saveset_summaries]

        self.current_saveset_files = saveset_files_mod.Saveset_files(self)

        # I tried making this 100 * the number of source savesets, but it was overwhelming a machine with 1 gig of
        # memory sometimes, so we instead use a smaller number.
        self.database_cache = cacher_mod.Database_cacher(max_entries=50)

    def set_up_file_count_estimate(self):
        """Get a file count estimate, by one way or another."""
        file_count_estimate = pick_file_count_estimate(
            self.prior_saveset_summaries,
            10000000,
            file_count_mod.File_count.file_count,
        )

        self.hardlinks = hardlinks_mod.Save_hardlinks(self.backup_id, file_count_estimate)

    def to_established_backup_id(self, backup_id):
        """Read in basic stuff describing a backupid, from a preexisting backup id."""
        self.reading = True

        self.backup_id = backup_id
        self.current_saveset_summary = saveset_summary_mod.Saveset_summary(
            'summaries',
            self.canonical_hostname,
            self.backup_id,
        )

        self.set_up_paths2()

    def create_new_backupid(self, init_savedir):
        """Create a new backupid within the repo."""
        self.writing = True

        self.current_saveset_summary = saveset_summary_mod.Saveset_summary(
            'summaries',
            self.canonical_hostname,
            subset=self.subset,
            init_savedir=init_savedir,
        )
        self.backup_id = self.current_saveset_summary.backup_id

        self.set_up_paths2()

    def get_metadata(self, filename):
        """List the content of a single backup."""
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)
        initial_directory = get_initial_directory(self.backup_id, dirname, shorten=True)
        files_path = os.path.join(initial_directory, constants_mod.Constants.s_entries)

        directory_content = db_mod.open(files_path, 'rb', backend_open=compressed_file_mod.Compressed_file)
        if basename in directory_content:
            print(directory_content[basename])
        else:
            sys.stderr.write('%s: %s does not exist in %s\n' % (sys.argv[0], basename, initial_directory))
            directory_content.close()
            sys.exit(1)
        directory_content.close()
        sys.exit(0)

    def list_backup(self, backup_id, starting_directory, recursive=True):
        """List the content of a single backup."""
        hardlink_data = hardlinks_mod.Restore_hardlinks(backup_id)
        self.traverse(backup_id, starting_directory, display_tvf, hardlink_data, recursive=recursive)
        # FIXME: Now we should optionally go through hardlink_data and warn about any hardlinks that don't show an ideal count

    def list_backup_simply(self, backup_id, starting_directory, recursive=True):
        """List the content of a single backup."""
        hardlink_data = hardlinks_mod.Restore_hardlinks(backup_id)
        self.traverse(backup_id, starting_directory, display_tf, hardlink_data, recursive=recursive)
        # FIXME: Now we should optionally go through hardlink_data and warn about any hardlinks that don't show an ideal count

    def produce_tar(self, backup_id, starting_directory, recursive=True, tar_format='default'):
        """Produce a tar archive from a backup id and starting directory, for restore or offsite backup."""
        hardlink_data = hardlinks_mod.Restore_hardlinks(backup_id)
        stdout = bufsock.rawio(handle=sys.stdout.fileno())

        if tar_format not in VALID_TAR_FORMATS:
            raise SystemExit('{}: internal error: tar_format {} not in valid_tar_formats'.format(sys.argv[0], tar_format))

        try:
            # We cannot use a "wb|" here - tarfile doesn't do that
            tar = tarfile.open(fileobj=stdout, mode="w|", bufsize=1048576, encoding='UTF-8', format=VALID_TAR_FORMATS[tar_format])
        except TypeError:
            list_ = [platform.python_implementation()] + list(platform.python_version_tuple())
            sys.stderr.write('Encoding issue in %s\n' % tuple(list_))
            raise

        tar_state = Tar_state(tar, hardlink_data)
        self.traverse(backup_id, starting_directory, give_tar, tar_state, recursive=recursive)
        tar.close()
        # FIXME: Now we should optionally go through tar_state.hardlink_data and warn about any hardlinks that
        # don't show an ideal count

#    def chdir(self):
#        """Change directory to the save directory - our files, chunks and summaries directories are under here"""
#        self.cd_count += 1
#        if self.cd_count > 1:
#            raise AssertionError("Too many cd's")
#        os.chdir(self.absolute_save_directory)

    def traverse(self, backup_id, starting_directory, visit, visit_arg=None, recursive=True):
        # pylint: disable=R0914,R0913
        # R0914: We seem to require a number of locals
        # R0913: We need a few arguments
        """
        Traverse the content of a single backup.

        This probably should use os.walk and not os.path.walk, because both are present in Python 2.x, but only os.walk
        is present in 3.x.  Some os.path.walk doc on the web says "Note This function is deprecated and has been removed
        in 3.0 in favor of os.walk()." - from http://docs.python.org/library/os.path.html .

        There's os.walk doc here: http://docs.python.org/library/os.html#os.walk
        """
        initial_directory = get_initial_directory(backup_id, starting_directory, shorten=False)
        for internal_root_dir, list_of_dirs, list_of_files in os.walk(initial_directory, topdown=True):
            if recursive:
                make_used(list_of_dirs)
            else:
                del list_of_dirs[:]
            # Strip off the 'files' directory and backup id directory, and the "./"
            slash = os.path.sep
            if slash == '\\':
                slash = '\\\\'
            internal_root_dir_path_parts, final = dirops_mod.get_path_parts(internal_root_dir)
            internal_root_dir_path_parts.append(final)
            stripped_root_dir = os.path.join(*internal_root_dir_path_parts[2:])
            if constants_mod.Constants.s_entries in list_of_files:
                user_root_dir = dirops_mod.strip_dirs(helpers.string_to_binary(stripped_root_dir))
                files_path = os.path.join(internal_root_dir, constants_mod.Constants.s_entries)
                # Here too: This is the "metadata is compressed" option for reading
                directory_content = db_mod.open(files_path, 'rb', backend_open=compressed_file_mod.Compressed_file)
                keys = list(directory_content.keys())
                keys.sort()
                for key in keys:
                    if user_root_dir == constants_mod.Constants.b_dot:
                        filename = key
                    else:
                        filename = os.path.join(user_root_dir, key)
                    backshift_file = backshift_file_mod.Backshift_file(self, directory_content[key], filename)
                    visit(backshift_file, visit_arg)
                directory_content.close()

    def list_backups(self, last_n):
        """List the backups in a repo."""
        saveset_summaries = saveset_summary_mod.get_all_saveset_summaries(self.save_directory, self.canonical_hostname, last_n)

        max_backup_id_width = 0
        max_number_of_files_width = 0
        for saveset_summary in saveset_summaries:
            len_backup_id_width = len(saveset_summary.backup_id)
            len_number_of_files_width = len(str(saveset_summary.number_of_files))
            if max_backup_id_width < len_backup_id_width:
                max_backup_id_width = len_backup_id_width
            if max_number_of_files_width < len_number_of_files_width:
                max_number_of_files_width = len_number_of_files_width

        for saveset_summary in saveset_summaries:
            string = ('%-*s %s %*d %s\n' % (
                max_backup_id_width,
                saveset_summary.backup_id,
                format_time(saveset_summary.start_time),
                max_number_of_files_width,
                saveset_summary.number_of_files,
                format_time(saveset_summary.finish_time),
            ))
            try:
                os.write(sys.stdout.fileno(), helpers.string_to_binary(string))
            except IOError as os_write_info:
                if os_write_info.errno == errno.EPIPE:
                    sys.exit(0)
                else:
                    raise

    def save_chunks(self, lstat_result, filename, dict_):
        """
        Save the chunks of a file - by borrowing from a previous backup, or computing the hashes the hard way.

        If we do the backup of this file the long and hard way, we return False.
        If we do the backup of this file the quick and easy way, we return True.
        """
        # Attempt to find a prior backup that contains this same pathname
        # that is also a regular file
        prior_backshift_file = None
        found_previous = False
        for saveset_files in self.prior_saveset_files:
            prior_backshift_file = saveset_files.get_filename(filename)
            # This seems like a lot of constraints, but actually, it should
            # happen a lot.
            #
            # Note that some Python's give mtimes to a resolution of 0.01,
            # while others give it to a resolution of 0.000001 - this could
            # cause some issues when switching from one python interpreter
            # to another.
            if prior_backshift_file is not None:
                # Promising: we found a file
                if prior_backshift_file.dict_.get(constants_mod.Constants.b_hash) is not None:
                    # And it's a non-zero length regular file too - even more promising

                    bs_file_mtime = prior_backshift_file.dict_[constants_mod.Constants.b_st_mtime]
                    dict_file_mtime = dict_[constants_mod.Constants.b_st_mtime]

                    bs_file_size = prior_backshift_file.dict_[constants_mod.Constants.b_st_size]
                    dict_file_size = dict_[constants_mod.Constants.b_st_size]

                    if abs(bs_file_mtime - dict_file_mtime) < 1e-2 and bs_file_size == dict_file_size:
                        # And it's even got the same modification time and the same length - use it!
                        found_previous = True
                        break

        if found_previous:
            try:
                borrow_and_save_chunks(dict_, prior_backshift_file)
            except Missing_chunk:
                found_previous = False
            else:
                return '%*s' % (constants_mod.Constants.file_type_width, 'mtime')

        if not found_previous:
            return '%*s' % (constants_mod.Constants.file_type_width, generate_and_save_chunks(lstat_result, filename, dict_))

        return 'n/a'

    def put_filename(self, filename, verbose=False):
        # pylint: disable=R0911
        # R0911: We benefit from a bunch of return statements
        """Save a file's metadata, and save the file's chunks."""
        try:
            lstat_result = os.lstat(filename)
        except OSError as cd_extra:
            if cd_extra.errno == errno.ENOENT:
                sys.stderr.write('File disappeared prior to lstat: Skipping %s\n' % filename)
                return
            elif cd_extra.errno == errno.EACCES:
                sys.stderr.write("File not lstat'able: Skipping %s\n" % filename)
                return
            else:
                raise

        # This gets all the metadata into an in-memory datastructure, but also has the side-effect of saving chunks if
        # they aren't already present
        try:
            backshift_file = backshift_file_mod.Backshift_file(repo=self, file_=lstat_result, filename=filename, verbose=verbose)
        except backshift_file_mod.Problematic_skipped as skip_extra:
            # this is a file to skip
            sys.stderr.write('Skipped important file: %s\n' % skip_extra)
            return
        except backshift_file_mod.Unknown_skipped as skip_extra:
            # this is a file to skip
            sys.stderr.write('Skipped unknown filetype: %s\n' % skip_extra)
            return
        except backshift_file_mod.Benign_skipped:
            # Ignore these - they're just things like unix domain sockets that'll be recreated when a process is restarted
            return
        except Permission_denied as permission_denied_extra:
            # this is a file to skip
            sys.stderr.write('Permission denied: %s\n' % permission_denied_extra)
            return

        if self.writing and stat.S_ISREG(lstat_result.st_mode):
            # This is a regular file, so add it to our collection of (potential) hardlinks
            self.hardlinks += (lstat_result.st_dev, lstat_result.st_ino)

        # Now we save the metadata
        self.current_saveset_files.put_filename(filename, backshift_file)

        self.files_saved += 1
        self.current_saveset_summary.update(number_of_files=self.files_saved)

    def close(self):
        """Close the repo."""
# This is done by saveset.update(finished=True) now
#        if self.saveset_file is not None and self.writing:
#            self.saveset_file.write('finished %s\n' % current_time())
#            self.saveset_file.close()

        # Here we really do want to close our databases...  They've served their purpose by now.
        if self.database_cache is not None:
            self.database_cache.close()

        if self.current_saveset_summary is not None:
            self.current_saveset_summary.close()

        if self.hardlinks is not None:
            self.hardlinks.close()

        if self.writing:
            sys.stderr.write('%s\n' % self.speeds)

#    def __enter__(self):
#        return self
#
#    def __exit__(self, type_, value, traceback):
#        if value is None:
#            self.close()
#            return True
#        else:
#            return False
