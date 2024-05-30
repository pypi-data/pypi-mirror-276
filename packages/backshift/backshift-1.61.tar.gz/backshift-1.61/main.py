#!/usr/bin/env python

# pylint: disable=simplifiable-if-statement
# simplifiable-if-statement: I think it's more clear to do the if
# redefined-variable-type: We want STDIN to be different types

"""Backshift: A deduplicating backup script with expiration."""

import errno
import os
import sys
import time

import chunk_mod
import constants_mod
import expire_mod
import file_count_mod
import get_chunk
import helpers
import modunits
import readline0
import repo_mod
import saveset_summary_mod

STDIN = 0


def usage(retval):
    """Print a usage message, exit with passed exit code."""
    if retval == 0:
        ssw = sys.stdout.write
    else:
        ssw = sys.stderr.write
    ssw("%s: Usage:\n" % sys.argv[0])
    ssw("\t--save-directory /directory/for/saved/data   - where is the repository?  for most operations                    \n")
    ssw('\t--init-savedir                               - initialize the save directory for use - nondestructive           \n')
    ssw("\t--backup                                     - perform a backup                                                 \n")
    ssw('\t--filelist filename                          - get input filenames from filename instead of stdin               \n')
    ssw("\t--list-backups                               - list the backups in the repo                                     \n")
    ssw("\t--last-n                                     - specify the number of backups to list                            \n")
    ssw("\t--list-backup                                - list the content of a specific backup in the repo - like tar tvf \n")
    ssw("\t--list-backup-simply                         - like --list-backup, but - just the filenames -      like tar tf  \n")
    ssw('\t--starting-directory /first/dir              - directory to start in; for --list-backup or --produce-tar: (".") \n')
    ssw("\t--backup-id                                  - which backup id to list or restore                               \n")
    ssw("\t--progress-report arg                        - type of progress info to show during a backup.  Default is       \n")
    ssw('\t                                               full+poststat.\n')
    ssw('\t   none                             : give no progress report                                                   \n')
    ssw('\t   minimal                          : give a minimal progress report with file count and files/second           \n')
    ssw('\t   moderate                         : give a moderately nice progress report with files/second and ETA          \n')
    ssw('\t   full+poststat                    : give a nice progress report with bytes/second and ETA; backshift gets size\n')
    ssw('\t   full+prestat                     : give a nice progress report with bytes/second and ETA; find gets size     \n')
    ssw('\n')
    ssw("\t--produce-tar                                - restore from backupid                                            \n")
    ssw('\t   --tar-format arg                          - specify version of tar to use for --produce-tar                  \n')
    ssw('\t      ustar                         : use old ustar format. Good for broad compatibility, limited               \n')
    ssw('\t      gnu                           : use gnu format. Best compatibility with GNU tar, good for tar --diff ?    \n')
    ssw('\t      pax                           : use pax (POSIX) format. few arbitrary limits?                             \n')
    ssw("\t--hostname hostname                          - specify a hostname (for when reverse resolution is not useful)   \n")
    ssw("\t--subset subset                              - specify a subset (aids detecting which saveset to base an\n")
    ssw('\t                                               incremental on) \n')
    ssw('\t--expire [--check-hashes]           : Remove too-old chunks.  Remove 0 length (bad) chunks.  [Compare hashes]   \n')
    ssw('\t--get-chunk                         : Output one hash to stdout - not always an entire "file".\n')
    ssw('\t--get-metadata                      : Output one file\'s metadata to stdout\n')
    ssw('\t--nonrecursive                      : with --list-backup or --produce-tar, do not operate recursively  \n')
    ssw('\t--compression-means                 : Report the means of compression\n')
    ssw('\n')
    ssw('To do a fullsave of your root filesystem, pipe "find / -xdev -print0" into me - possibly pruning the things that  \n')
    ssw("are volatle like TMPFS's.  You could elide cache directories too, if you feel like it, using -prune.\n")
    ssw('\n')
    ssw('To backup your own home directory, pipe "find $HOME -xdev -print0" into me.\n')
    sys.exit(retval)


class Progress_report(object):
    # pylint: disable=R0903
    # R0903: We don't require a lot of public methods
    """A class for describing what kind of progress report to give during a backup."""

    _none, _minimal, _moderate, _full_prestat, _full_poststat = range(5)

    def __init__(self, type_):
        """Initialize."""
        if type_ == 'none':
            self.description = type_
            self.type_ = Progress_report._none
        elif type_ == 'minimal':
            self.description = type_
            self.type_ = Progress_report._minimal
        elif type_ == 'moderate':
            self.description = type_
            self.type_ = Progress_report._moderate
        elif type_ == 'full+prestat':
            self.description = type_
            self.type_ = Progress_report._full_prestat
        elif type_ == 'full+poststat':
            self.description = type_
            self.type_ = Progress_report._full_poststat
        else:
            string = 'Progress_report called with %s which is not none, minimal, moderate, full+prestat or full+poststat' % type_
            raise ValueError(string)

    def __cmp__(self, other):
        """Compare: the python 2.x way."""
        if self.type_ < other.type_:
            return -1
        elif self.type_ > other.type_:
            return 1
        elif self.type_ == other.type_:
            return 0
        else:
            raise AssertionError('Progress_report: Not <, > or ==?')

    def __lt__(self, other):
        """<: The Python 3 way."""
        return self.type_ < other.type_

    def __gt__(self, other):
        """>: The Python 3 way."""
        return self.type_ > other.type_

    def __eq__(self, other):
        """==: The Python 3 way."""
        return self.type_ == other.type_

    def __str__(self):
        """Convert to string."""
        return "Progress_report('%s')" % self.description


class Options(object):
    # pylint: disable=R0913,R0903,R0902
    # R0913: We want lots of arguments
    # R0903: We don't need a lot of public methods; we're a container
    # R0902: We need a bunch of instance attributes; we're a container
    """Just hold our command line options."""

    def __init__(self):
        """Initialize."""
        self.save_directory = None
        self.starting_directory = '.'
        self.backup = False
        self.produce_tar = False
        self.progress_report = Progress_report('full+poststat')
        self.list_backups = False
        self.list_backup = False
        self.list_backup_simply = False
        self.recursive = True
        self.expire = False
        self.check_hashes = False
        self.backup_id = None
        self.user_hostname = None
        self.subset = None
        self.init_savedir = False
        self.compression_means = False
        self.last_n = None
        self.get_chunk = False
        self.hash_string = ''
        self.hash_string = ''
        self.get_metadata = False
        self.filename = b''
        # default to STDIN
        self.filelist = None
        self.tar_format = 'default'


def check_options(options):
    # pylint: disable=too-many-branches,too-many-statements
    """Make sure the options combine well - error out if not."""
    total = (
        options.backup +
        options.list_backups +
        options.list_backup +
        options.list_backup_simply +
        options.produce_tar +
        options.expire +
        options.compression_means +
        options.get_chunk +
        options.get_metadata)
    if total != 1:
        sys.stderr.write('Must specify exactly one of\n')
        sys.stderr.write('\t--backup\n\t--list-backups\n\t--produce-tar\n\t--expire\n\t--compression-means\n\t--get-chunk\n')
        sys.stderr.write('\t--get-metadata\n\n')
        sys.stderr.write("--backup: %s\n" % options.backup)
        sys.stderr.write("--list-backups: %s\n" % options.list_backups)
        sys.stderr.write("--list-backup: %s\n" % options.list_backup)
        sys.stderr.write("--list-backup-simply: %s\n" % options.list_backup_simply)
        sys.stderr.write("--produce-tar: %s\n" % options.produce_tar)
        sys.stderr.write("--expire: %s\n" % options.expire)
        sys.stderr.write("--compression-means: %s\n" % options.compression_means)
        sys.stderr.write("--get-chunk: %s\n" % options.get_chunk)
        sys.stderr.write("--get-metadata: %s\n" % options.get_chunk)
        usage(1)

    if not (options.list_backup or options.list_backup_simply or options.produce_tar) and not options.recursive:
        sys.stderr.write('--nonrecursive is only relevant with --list-backup or --produce-tar\n')
        sys.stderr.write('options.list_backup: %s\n' % options.list_backup)
        sys.stderr.write('options.list_backup_simply: %s\n' % options.list_backup_simply)
        sys.stderr.write('options.produce_tar: %s\n' % options.produce_tar)
        sys.stderr.write('options.recursive  : %s\n' % options.recursive)
        usage(1)

    if options.backup and not options.subset:
        sys.stderr.write('--backup necessitates --subset\n')
        usage(1)

    if not options.backup and options.filelist is not None:
        sys.stderr.write('--filelist filename only works with --backup')
        usage(1)

    if (options.backup or
            options.list_backup or
            options.list_backup_simply or
            options.list_backups) and not options.save_directory:
        sys.stderr.write('--backup, --list-backup, --list-backup-simply and --list-backups require --save-directory\n')
        usage(1)

    if (options.list_backup or
            options.list_backup_simply or
            options.produce_tar or
            options.get_metadata) and not options.backup_id:
        sys.stderr.write('--list-backup, --list-backup-simply, --produce-tar and --get-metadata require --backup-id\n')
        usage(1)

    if options.check_hashes and not options.expire:
        sys.stderr.write('--check-hashes requires --expire\n')
        usage(1)

    if options.last_n is not None:
        if not options.list_backups:
            sys.stderr.write('--last-n requires --list-backups\n')
            usage(1)

    if options.get_chunk and options.hash_string == '':
        sys.stderr.write('Internal error: options.get_chunk but no options.hash_string\n')
        sys.exit(1)

    if options.get_metadata:
        if options.filename == '':
            sys.stderr.write('Internal error: options.get_metadata but no options.filename\n')
            sys.exit(1)
        if options.backup_id == '':
            sys.stderr.write('Internal error: options.get_metadata but no options.filename\n')
            sys.exit(1)

    if options.produce_tar:
        if options.tar_format in repo_mod.VALID_TAR_FORMATS:
            # Good, we have a valid tar format to use.
            pass
        else:
            sys.stderr.write('--tar-format accepts the following formats:\n')
            for valid_tar_format in repo_mod.VALID_TAR_FORMATS:
                sys.stderr.write('   {}\n'.format(valid_tar_format))
            usage(1)


def parse_options():
    # pylint: disable=R0912,too-many-statements
    # R0912: We need a bunch of branches
    """Stick the command line options in a container as useful variables."""
    options = Options()

    while sys.argv[1:]:
        if sys.argv[1] == '--save-directory':
            options.save_directory = os.path.abspath(sys.argv[2])
            del sys.argv[1]
        elif sys.argv[1] == '--init-savedir':
            options.init_savedir = True
        elif sys.argv[1] == '--starting-directory':
            options.starting_directory = sys.argv[2]
            if not os.path.isabs(options.starting_directory):
                sys.stderr.write('--starting-directory must be an absolute path\n')
                usage(1)
            del sys.argv[1]
        elif sys.argv[1] == '--hostname' and sys.argv[2:]:
            options.user_hostname = sys.argv[2]
            del sys.argv[2]
        elif sys.argv[1] == '--subset' and sys.argv[2:]:
            options.subset = sys.argv[2]
            del sys.argv[2]
        elif sys.argv[1] == '--backup':
            options.backup = True
        elif sys.argv[1] == '--list-backups':
            options.list_backups = True
        elif sys.argv[1] == '--last-n':
            options.last_n = int(sys.argv[2])
            del sys.argv[1]
        elif sys.argv[1] == '--list-backup':
            options.list_backup = True
        elif sys.argv[1] == '--list-backup-simply':
            options.list_backup_simply = True
        elif sys.argv[1] == '--expire':
            options.expire = True
        elif sys.argv[1] == '--compression-means':
            options.compression_means = True
        elif sys.argv[1] == '--get-chunk':
            options.get_chunk = True
            options.hash_string = sys.argv[2]
            del sys.argv[1]
        elif sys.argv[1] == '--get-metadata':
            options.get_metadata = True
            options.filename = helpers.string_to_binary(sys.argv[2])
            del sys.argv[1]
        elif sys.argv[1] == '--get-metadata':
            options.get_metadata = True
            options.filename = sys.argv[2]
            del sys.argv[1]
        elif sys.argv[1] == '--check-hashes':
            options.check_hashes = True
        elif sys.argv[1] == '--filelist' and sys.argv[2:]:
            options.filelist = open(sys.argv[2], 'rb')
            del sys.argv[1]
        elif sys.argv[1] == '--backup-id' and sys.argv[2:]:
            options.backup_id = sys.argv[2]
            # this is a very rudimentary test to see if the user has given a valid backup id
            if options.backup_id[0] not in '0123456789':
                sys.stderr.write('--backup-id must specify a backup id from the first column of --list-backups\n')
                usage(1)
            del sys.argv[1]
        elif sys.argv[1] == '--progress-report':
            options.progress_report = Progress_report(sys.argv[2])
            del sys.argv[1]
        elif sys.argv[1] == '--produce-tar':
            options.produce_tar = True
        elif sys.argv[1] == '--nonrecursive':
            options.recursive = False
        elif sys.argv[1] == '--tar-format':
            options.tar_format = sys.argv[2]
            del sys.argv[1]
        elif sys.argv[1] in ['--help', '-h']:
            usage(0)
        else:
            sys.stderr.write('%s: Illegal option: %s\n' % (sys.argv[0], sys.argv[1]))
            usage(1)
        del sys.argv[1]

    check_options(options)

    return options


def strip_start(string, possible_prefixes):
    """
    Strip a prefix.

    If string starts with one of the prefixes in possible_prefixes, strip off the prefix and return it.
    Otherwise, return the string unchanged.
    """
    for possible_prefix in possible_prefixes:
        binary_possible_prefix = helpers.string_to_binary(possible_prefix)
        if string.startswith(binary_possible_prefix):
            return string[len(binary_possible_prefix):]
    return string


def absolutize(directory_at_outset, filename):
    """
    Make a filename absolute.

    If filename is relative, make it absolute relative to the CWD when the program was started,
    as indicated by directory_at_outset
    """
    dotless_filename = strip_start(filename, ['.%s' % os.path.sep, '.%s' % os.path.altsep])

    if not os.path.isabs(dotless_filename):
        absolute_filename = os.path.join(directory_at_outset, dotless_filename)
    else:
        absolute_filename = dotless_filename

    return absolute_filename


def ascii_ize(binary):
    """Replace non-ASCII characters with question marks; otherwise writing to sys.stdout tracebacks."""
    list_ = []
    question_mark_ordinal = ord('?')
    for ordinal in binary:
        if 0 <= ordinal <= 127:
            list_.append(ordinal)
        else:
            list_.append(question_mark_ordinal)
    return bytes(list_)


def output_filename(filename, add_eol=True):
    """Output a filename to the tty (stdout), taking into account that some tty's do not allow non-ASCII characters."""
    replaced1 = filename.replace(constants_mod.Constants.b_newline, constants_mod.Constants.b_question)
    replaced2 = replaced1.replace(constants_mod.Constants.b_cr, constants_mod.Constants.b_question)
    replaced3 = replaced2.replace(constants_mod.Constants.b_tab, constants_mod.Constants.b_question)
    replaced4 = ascii_ize(replaced3)

    # This gives errors on /etc/ssl/certs/T??B??TAK_UEKAE_K??k_Sertifika_Hizmet_Sa??lay??c??s??_-_S??r??m_3.pem
    # with sys.stdout.write
    os.write(sys.stdout.fileno(), replaced4)

    if add_eol:
        os.write(sys.stdout.fileno(), constants_mod.Constants.b_newline)


def backup_moderate_stats(filelist, repo, directory_at_outset):
    """
    Create a backup with moderate progress output.

    Inhale the filenames, and give a percent complete by bytes as we go.  We pretend every byte takes
    the same amount of time.
    """
    filenames = []
    for filenameno, filename in enumerate(readline0.readline0(file_=filelist)):
        if filenameno and filenameno % 10000 == 0:
            string = 'Inhaled %d filenames for progress report - you can use --progress-report nothing or ' + \
                '--progress-report minimal to disable inhalation\n'
            os.write(sys.stdout.fileno(), helpers.string_to_binary(string % filenameno))
        filename = absolutize(directory_at_outset, filename)
        filenames.append(filename)
    num_filenames = len(filenames)
    file_count_mod.File_count.file_count = num_filenames
    repo.set_up_file_count_estimate()
    time0 = time.time()
    for filenameno, filename in enumerate(filenames):
        repo.put_filename(filename, verbose=True)
        time1 = time.time()
        delta_time = time1 - time0
        # High school algebra: A proportion to compute when the backup should complete,
        # assuming that the various file sizes are evenly distributed (which isn't always
        # true, but a statistic that isn't perfect is frequently better than no statistic,
        # in this case).
        #
        # filenameno        time1-time0
        #  -------       = -------------
        # num_filenames     finish_time-time0
        #
        # filenameno*(finish_time - time0) == num_filenames*(time1 - time0)
        # finish_time - time0 == num_filenames*(time1 - time0) / filenameno
        # finish_time == num_filenames * (time1 - time0) / filenameno + time0
        if delta_time and filenameno:
            finish_time = num_filenames * delta_time / filenameno + time0
            string = '%6.2f%% done, %.2f files/second, ETA %s, ' % (
                (float(filenameno) * 100.0) / num_filenames,
                filenameno / delta_time,
                time.ctime(finish_time))
            binary = helpers.string_to_binary(string)
            os.write(sys.stdout.fileno(), binary)
        output_filename(filename)


def get_full_prestat_progress_recs(filelist, repo, directory_at_outset):
    r"""Read the records for a full+prestat progress report.  Assume we'll get sizeblankfilename\0 on each line of input."""
    records = []
    for filenameno, line in enumerate(readline0.readline0(file_=filelist)):
        partitioned = line.partition(constants_mod.Constants.b_blank)
        if len(partitioned) != 3 or partitioned[1] != constants_mod.Constants.b_blank:
            sys.stderr.write('full+prestat progress report requested, but line %d does not contain a space.\n' % (filenameno + 1))
            sys.stderr.write('Did you neglect to use, EG "find / -xdev -printf \'%%s %%p\\0\'"?\n')
            sys.exit(1)
        file_size = int(partitioned[0])
        filename = partitioned[2]
        if filenameno and filenameno % 10000 == 0:
            string = 'Inhaled %d filenames for progress report - can use --progress-report minimal to disable inhalation' % \
                filenameno
            os.write(sys.stdout.fileno(), '%s\n' % (string, ))
        filename = absolutize(directory_at_outset, filename)
        tuple_ = (file_size, filename)
        records.append(tuple_)
    num_records = len(records)
    file_count_mod.File_count.file_count = num_records
    repo.set_up_file_count_estimate()
    return (num_records, records)


def get_full_poststat_progress_recs(filelist, repo, directory_at_outset):
    """
    Produce a backup with poststat progress.

    Read the records for a full+poststat progress report.  Use stat to compute file sizes before we start backing anything up.
    """
    records = []
    for filenameno, filename in enumerate(readline0.readline0(file_=filelist)):
        absolute_filename = absolutize(directory_at_outset, filename)
        try:
            # Jython 2.7.0 raises an OSError for filenames having bytes that do not decode to unicode. It uses a unicode
            # replacement character.
            # http://bugs.jython.org/issue2239
            # It is reasonable to hope that jython 3.x will support this better. It's possible, though perhaps not
            # likely that it will be fixed in 2.7.x at some point.
            stat_buf = os.lstat(absolute_filename)
        except (OSError, IOError) as size_extra:
            if size_extra.errno == errno.ENOENT:
                sys.stderr.write('Skipping missing file: %s (%d)\n' % (filename, len(filename)))
                continue
            elif size_extra.errno == errno.EACCES:
                sys.stderr.write('Skipping inaccessible file: %s (%d)\n' % (filename, len(filename)))
                continue
            elif size_extra.errno == errno.ESTALE:
                sys.stderr.write('Skipping stale handle: %s (%d)\n' % (filename, len(filename)))
                continue
            else:
                raise
        file_size = stat_buf.st_size
        if filenameno and filenameno % 10000 == 0:
            string = ('Inhaled %d filenames for progress report - can use --progress-report minimal ' % filenameno)
            string += 'to disable inhalation\n'
            os.write(sys.stdout.fileno(), helpers.string_to_binary(string))
        tuple_ = (file_size, absolute_filename)
        records.append(tuple_)
    num_records = len(records)
    file_count_mod.File_count.file_count = num_records
    repo.set_up_file_count_estimate()
    return (num_records, records)


def backup_full_prestat_stats(filelist, repo, directory_at_outset):
    """Do a backup - assume find has prefixed filenames with sizes separated by a space."""
    return backup_full_progress_report(filelist, repo, directory_at_outset, get_full_prestat_progress_recs)


def backup_full_poststat_stats(filelist, repo, directory_at_outset):
    """Do a backup - assume find lists filenames only - we add the sizes."""
    return backup_full_progress_report(filelist, repo, directory_at_outset, get_full_poststat_progress_recs)


def backup_full_progress_report(filelist, repo, directory_at_outset, get_records):
    # pylint: disable=too-many-locals
    """
    Produce a backup.  Inhale the filenames, and give a percent complete as we go.

    We treat bytes in a file as bytes in a file, and metadata is always assumed metadata_size bytes.
    """
    num_records, records = get_records(filelist, repo, directory_at_outset)

    # We pretend that the metadata for each file is 100 bytes long, because we don't want millions of 0 length files
    # to be estimated as nothing!
    metadata_size = 100
    total_size = sum(tuple_[0] for tuple_ in records) + num_records * metadata_size
    time0 = time.time()
    size_so_far = 0
    for recordno, (file_size, filename) in enumerate(records):
        repo.put_filename(filename, verbose=True)
        time1 = time.time()
        delta_time = time1 - time0

        # size_so_far   delta_time
        # ----------- = ----------
        # total_size    total_time
        #
        # size_so_far * total_time = total_size * delta_time
        # total_time = total_size * delta_time / size_so_far
        size_so_far += file_size + metadata_size
        if delta_time and recordno:
            total_duration = total_size * delta_time / size_so_far
            string = '%6.2f%% done, %s, ETA %s, ' % (
                (float(size_so_far) * 100.0) / total_size,
                modunits.modunits(
                    'computer-bits-per-second-si',
                    float(size_so_far) * 8.0 / delta_time,
                    units='unabbreviated',
                    fractional_part_length=2,
                ),
                time.ctime(time0 + total_duration),
            )
            os.write(sys.stdout.fileno(), helpers.string_to_binary(string))
        output_filename(filename)


def backup_no_stats(filelist, repo, directory_at_outset):
    """Produce a backup.  Don't inhale the filenames, and don't give a percent complete as we go."""
    repo.set_up_file_count_estimate()
    for filename in readline0.readline0(file_=filelist):
        filename = absolutize(directory_at_outset, filename)
        repo.put_filename(filename)


def backup_minimal_stats(filelist, repo, directory_at_outset):
    """Produce a backup.  Don't inhale the filenames, and don't give a percent complete as we go."""
    repo.set_up_file_count_estimate()
    time0 = time.time()
    for fileno, filename in enumerate(readline0.readline0(file_=filelist)):
        filename = absolutize(directory_at_outset, filename)
        repo.put_filename(filename)
        time1 = time.time()
        delta_t = time1 - time0
        if delta_t:
            os.write(sys.stdout.fileno(), 'File #%d, %.2f files/second %s\n' % (
                fileno,
                float(fileno) / delta_t,
                helpers.binary_to_string(filename),
            ))
        else:
            os.write(sys.stdout.fileno(), 'File #%d, N/A files/second %s\n' % (fileno, helpers.binary_to_string(filename)))


def perform_expire(starting_directory, check_hashes):
    """Expire old chunks and savesets from a repository."""
    os.chdir(starting_directory)

    current_time = time.time()

    expire_mod.expire(current_time, check_hashes)


def perform_get_chunk(starting_directory, hash_string):
    """Output one chunk to stdout."""
    os.chdir(starting_directory)

    get_chunk.get_chunk(hash_string)


def perform_get_metadata(repo, backup_id, save_directory, filename):
    """Output one file's metadata to stdout."""
    os.chdir(save_directory)

    repo.to_established_backup_id(backup_id)
    repo.get_metadata(filename)


def perform_list_backups(repo, last_n):
    """List all the backups in a repository."""
    repo.list_backups(last_n)


def perform_list_backup(repo, backup_id, starting_directory, recursive=True):
    """List all files within a backup along the lines of 'tar tvf'."""
    repo.to_established_backup_id(backup_id)
    repo.list_backup(backup_id, starting_directory, recursive=recursive)


def perform_list_backup_simply(repo, backup_id, starting_directory, recursive=True):
    """List all files within a backup along the lines of 'tar tf'."""
    repo.to_established_backup_id(backup_id)
    repo.list_backup_simply(backup_id, starting_directory, recursive=recursive)


def produce_tar(repo, backup_id, starting_directory, recursive=True, tar_format='default'):
    """Dump content in tar format for restoration or offsite backup."""
    repo.to_established_backup_id(backup_id)
    repo.produce_tar(backup_id, starting_directory, recursive=recursive, tar_format=tar_format)


def handle_savedir(save_directory, init_savedir):
    """
    Maybe create savedir, maybe error about savedir - depending on init-savedir.

    We only create it if it doesn't yet exist, and init_savedir is True.
    """
    if init_savedir:
        if os.path.isdir(save_directory):
            sys.stderr.write('%s: %s already exists - are you saving to the correct place?\n' % (sys.argv[0], save_directory))
            sys.exit(1)
        else:
            os.mkdir(save_directory, 7 * 64 + 0 * 8 + 0 * 1)
    else:
        if os.path.isdir(save_directory):
            # Good thing
            pass
        else:
            sys.stderr.write('%s does not exist or is not a directory - please\n' % save_directory)
            sys.stderr.write('consider whether this is the right directory and if it is, then create it\n')
            sys.stderr.write('with --init-savedir.  It could be that a filesystem is not mounted.\n')
            usage(1)


def main():
    # pylint: disable=too-many-branches
    """
    Operations available follow.

    - perform a backup
    - restore a backup
    - list backups available
    - list files within a backup
    - or expire old files.
    """
    # Save this before we create a Repo instance, because creating a repo instance will cd to the save directory.
    # We don't always need this value, but it's inexpensive to retrieve it once.
    directory_at_outset = helpers.string_to_binary(os.getcwd())

    options = parse_options()

    if options.compression_means:
        import xz_mod
        os.write(sys.stdout.fileno(), helpers.string_to_binary('%s\n' % (xz_mod.MEANS, )))
        sys.exit(0)

    if options.filelist is None:
        options.filelist = STDIN

    handle_savedir(options.save_directory, options.init_savedir)

    canonical_hostname = saveset_summary_mod.canonicalize_hostname(options.user_hostname)

    repo = repo_mod.Repo(options.save_directory, canonical_hostname, options.subset)
    if options.backup:
        repo.create_new_backupid(options.init_savedir)
        if options.progress_report == Progress_report('none'):
            backup_no_stats(options.filelist, repo, directory_at_outset)
        elif options.progress_report == Progress_report('minimal'):
            backup_minimal_stats(options.filelist, repo, directory_at_outset)
        elif options.progress_report == Progress_report('moderate'):
            backup_moderate_stats(options.filelist, repo, directory_at_outset)
        elif options.progress_report == Progress_report('full+prestat'):
            backup_full_prestat_stats(options.filelist, repo, directory_at_outset)
        elif options.progress_report == Progress_report('full+poststat'):
            backup_full_poststat_stats(options.filelist, repo, directory_at_outset)
        else:
            raise ValueError('options.progress_report has strange value: %s' % options.progress_report)
    elif options.list_backups:
        perform_list_backups(repo, options.last_n)
    elif options.list_backup and options.backup_id:
        perform_list_backup(repo, options.backup_id, options.starting_directory, options.recursive)
    elif options.list_backup_simply and options.backup_id:
        perform_list_backup_simply(repo, options.backup_id, options.starting_directory, options.recursive)
    elif options.produce_tar:
        produce_tar(repo, options.backup_id, options.starting_directory, options.recursive, tar_format=options.tar_format)
    elif options.expire:
        perform_expire(options.starting_directory, options.check_hashes)
    elif options.get_chunk:
        perform_get_chunk(options.starting_directory, options.hash_string)
    elif options.get_metadata:
        perform_get_metadata(
            repo=repo,
            backup_id=options.backup_id,
            save_directory=options.save_directory,
            filename=options.filename,
        )
    else:
        sys.stderr.write("Internal error\n")
        sys.exit(1)
    repo.close()
    chunk_mod.finalize()
