#!/usr/bin/env python

# pylint: disable=simplifiable-if-statement

"""Provides a class and related functions for operating on savesets."""

import os
import re
import sys
import time
import random
import socket
import decimal
import platform

import backshift_os_mod

CHECKPOINT_MULTIPLE = 1000

SUMMARIES_NAME = 'summaries'


def decimal_round(decimal_value, hundredths=decimal.Decimal('0.01')):
    """Round a decimal value to 2 places after the decimal point."""
    return decimal_value.quantize(hundredths, rounding=decimal.ROUND_HALF_EVEN)


def canonicalize_hostname(user_hostname=None):
    """Return the current machine's hostname - canonicalized."""
    bad_hostnames = ['localhost', 'localhost.localdomain']
    if user_hostname is None:
        non_canonical_hostname = platform.node()
        try:
            canonical_hostname = socket.gethostbyaddr(socket.gethostbyname(non_canonical_hostname))[0]
        except (socket.gaierror, socket.herror):
            canonical_hostname = 'localhost'
            assert canonical_hostname in bad_hostnames
        if canonical_hostname not in bad_hostnames:
            result = canonical_hostname
        elif non_canonical_hostname not in bad_hostnames:
            result = non_canonical_hostname
        else:
            raise AssertionError('user_hostname is None, and both canonical and noncanonical hostnames are blacklisted')
    else:
        result = user_hostname
    return result.lower()


def random_string(length=16):
    """Return a hexadecimal string of length length."""
    list_ = []
    for _unused in range(length):
        list_.append(random_hex_digit())
    return ''.join(list_)


def random_hex_digit():
    """Return a single, random hex digit."""
    return '0123456789abcdef'[int(random.random() * 16)]


def get_all_saveset_summaries(save_directory, canonical_hostname, last_n=None):
    """Get all the savesets, creating one Saveset object for each."""
    saveset_directory = os.path.join(save_directory, SUMMARIES_NAME)

    all_savesets_list = []

    # We skip temporary files, otherwise we'd see things twice sometimes, and get a traceback sometimes.
    files = [filename for filename in os.listdir(saveset_directory) if not filename.endswith('.temp')]
    files.sort(key=lambda filename: float(filename.split('_')[0]))
    if last_n is not None:
        files = files[-last_n:]  # pylint: disable=invalid-unary-operand-type

    for filename in files:
        saveset = Saveset_summary(saveset_directory, canonical_hostname, backup_id=filename)
        all_savesets_list.append(saveset)

    all_savesets_list.sort()

    return all_savesets_list


def backup_id_present(saveset_summary, saveset_summary_list):
    """Return True if saveset_summary's backup id is present in saveset_summary_list."""
    for candidate_summary in saveset_summary_list:
        if saveset_summary.backup_id == candidate_summary.backup_id:
            return True
    return False


def get_hostname_subset_matches(all_savesets_list, canonical_hostname, subset):
    """Get a list of saveset summaries that match on the hostname and subset."""
    hostname_subset_match_savesets = []

    for saveset in all_savesets_list:
        if saveset.canonical_hostname == canonical_hostname and saveset.subset == subset:
            # This is in the set we're interested in
            hostname_subset_match_savesets.append(saveset)

    return hostname_subset_match_savesets


def get_tweaked_matches(current_saveset_summary, hostname_subset_match_savesets):
    """Now exclude the current saveset, because doing a save relative to itself makes no sense."""
    tweaked_matches = []

    for saveset in hostname_subset_match_savesets:
        if saveset.backup_id == current_saveset_summary.backup_id:
            pass
        else:
            tweaked_matches.append(saveset)

    return tweaked_matches


def pick_saveset_summaries(save_directory, canonical_hostname, subset, current_saveset_summary):
    """Pick up to 3 savesets against which to perform an incremental."""
    all_savesets_list = get_all_saveset_summaries(save_directory, canonical_hostname)

    hostname_subset_match_savesets = get_hostname_subset_matches(all_savesets_list, canonical_hostname, subset)

    tweaked_matches = get_tweaked_matches(current_saveset_summary, hostname_subset_match_savesets)

    # for our hostname, subset tuple:
    # Pick the most recent (by start time) - whether complete or not
    most_recent_saveset = None
    for saveset in tweaked_matches:
        if most_recent_saveset is None or saveset.start_time > most_recent_saveset.start_time:
            most_recent_saveset = saveset

    # Pick the most recent (by start time) completed saveset with > 1 files in it - because
    # a backup of an empty mountpoint looks like a completed fullsave, but isn't.  And
    # if a save Should have only 1 file in it, we don't need to optimize that.
    most_recent_completed_saveset = None
    for saveset in tweaked_matches:
        tail = most_recent_completed_saveset is None or saveset.start_time > most_recent_completed_saveset.start_time
        if saveset.finish_time is not None and tail and saveset.number_of_files > 1:
            most_recent_completed_saveset = saveset

    # Pick the one with the most files in it - might not be a precise number, but should be
    # pretty close: % CHECKPOINT_MULTIPLE
    most_files_saveset = None
    for saveset in tweaked_matches:
        if most_files_saveset is None or saveset.number_of_files > most_files_saveset.number_of_files:
            most_files_saveset = saveset

    # create a list with the 3, but excluding duplicates - so it could get fewer than 3 elements
    list_ = []
    if most_recent_saveset is not None:
        list_.append(most_recent_saveset)
    if most_recent_completed_saveset is not None and not backup_id_present(most_recent_completed_saveset, list_):
        list_.append(most_recent_completed_saveset)
    if most_files_saveset is not None and not backup_id_present(most_files_saveset, list_):
        list_.append(most_files_saveset)

    # sort the list
    list_.sort()

    if list_:
        sys.stderr.write('Backing up relative to:\n')
        for element in list_:
            sys.stderr.write('   %s\n' % element.backup_id)
    else:
        sys.stderr.write('Found nothing to backup relative to.\n')

    # Attempt to get "backing up relative to" output near the beginning of looper subprocess,
    # not near the end.
    sys.stderr.flush()

    # Return the resulting list.
    # Note: if list_ is empty, this is a fullsave.
    return list_


def create_dir_if_needed(init_savedir):
    """Create the savesets directory if its needed."""
    # If the summaries directory does not yet exist
    if not os.path.isdir(SUMMARIES_NAME):
        # If the user requested save directory creation, create it.  Else, give a mostly-helpful error message.
        if init_savedir:
            os.mkdir(SUMMARIES_NAME)
        else:
            sys.stderr.write('summaries directory does not exist - rerun with --init-savedir option?\n')
            sys.exit(1)


class Saveset_summary(object):
    # pylint: disable=R0902
    # R0902: We need a handful of instance attributes
    """A class for summaries - both new and existing."""

    def __init__(self, directory, canonical_hostname, backup_id=None, subset=None, init_savedir=False):
        """Initialize."""
        # pylint: disable=R0913,too-many-statements
        # R0913: We seem to need a few arguments
        # too-many-statements: I'm willing to allow a large __init__ in this case.
        create_dir_if_needed(init_savedir)

        self.last_checkpoint_time = time.time()

        self.directory = directory
        if backup_id is None:
            self.new_saveset = True
            self.finished = False
            self.number_of_files = 0
            self.start_time = decimal.Decimal(str(time.time()))
            self.canonical_hostname = canonical_hostname
            assert subset is not None
            self.subset = subset
            self.random_string = random_string()
            self.backup_id = self.get_backup_id()
        else:
            # 1303099413.69_benchbox_slash_Sun-Apr-17-21-03-33-2    _ea7b44aa32d9fc64
            self.new_saveset = False
            fields = backup_id.split('_')
            self.start_time = decimal.Decimal(fields[0])
            self.canonical_hostname = fields[1]
            self.subset = fields[2]
            # we intentionally skip the human-readable form of the date, because we can easily get it back
            # from the machine-readable version
            self.random_string = fields[4]
            self.backup_id = backup_id
        self.backup_id_filename = os.path.join(self.directory, self.backup_id)
        self.temp_backup_id_filename = '%s.temp' % self.backup_id_filename
        if backup_id is None:
            sys.stderr.write('Creating backup id %s\n' % self.backup_id)
        else:
            file_ = open(self.backup_id_filename, 'r')
            for line in file_:
                saveset_fields = line.split()
                if saveset_fields[0] == 'start_time':
                    saveset_start_time = decimal.Decimal(saveset_fields[1])
                elif saveset_fields[0] == 'number_of_files':
                    self.number_of_files = int(saveset_fields[1])
                elif saveset_fields[0] == 'finish_time':
                    finish_time_string = saveset_fields[1]
                    # Note: We really do want 'None', not None
                    if finish_time_string == 'None':
                        self.finished = False
                        self.finish_time = None
                    else:
                        self.finished = True
                        self.finish_time = decimal.Decimal(finish_time_string)
            file_.close()
            saveset_start_time_2 = decimal_round(saveset_start_time)
            start_time_2 = decimal_round(self.start_time)
            if abs(saveset_start_time_2 - start_time_2) > decimal.Decimal('10.0'):
                sys.stderr.write('%s (type: %s) != %s (type: %s) - tolerance 10.0\n' % (
                    saveset_start_time_2,
                    type(saveset_start_time_2),
                    start_time_2,
                    type(start_time_2),
                ))
                sys.stderr.write('Filename is %s\n' % self.backup_id_filename)
                raise AssertionError('saveset_start_time_2 != self.start_time_2 within 10.0 tolerance')
            self.start_time = saveset_start_time
        if self.new_saveset:
            self.update(number_of_files=0)

    def __str__(self):
        """Convert to string."""
        if hasattr(self, 'finish_time'):
            finish_time = getattr(self, 'finish_time')
        else:
            finish_time = None
        return 'ss %s / %s / %d / %s' % (self.backup_id, self.start_time, self.number_of_files, finish_time)

    def __repr__(self):
        """Return a representation of this object."""
        return str(self)

    def __cmp__(self, other):
        """Sort by start_time and backup_id - the python 2 way."""
        if self.start_time < other.start_time:
            return -1
        if self.start_time > other.start_time:
            return 1
        if self.backup_id < other.backup_id:
            return -1
        if self.backup_id > other.backup_id:
            return 1
        return 0

    def __lt__(self, other):
        """Sort by start_time - the python 3 way."""
        if self.start_time < other.start_time:
            return True
        if self.backup_id < other.backup_id:
            return True
        return False

    def get_backup_id(self):
        """Create a backup id from this Saveset."""
        human_readable_time = re.sub('[ :]', '-', time.ctime(float(self.start_time)))
        elements = ['%.2f' % self.start_time, self.canonical_hostname, self.subset, human_readable_time, self.random_string]
        # we downcase the backup id, because otherwise case sense might cause issues
        # problems.
        return '_'.join(elements).lower()

    def checkpoint_interval_elapsed(self):
        """Return True iff it has been 10 minutes since we last checkpointed."""
        current_time = time.time()
        return self.last_checkpoint_time + 600 < current_time

    def update(self, number_of_files=None, finished=False):
        """Update the backup_id file content."""
        # note that finished and self.finished are two different things at this point in time
        if self.new_saveset:
            if number_of_files is not None:
                self.number_of_files = number_of_files
            if finished:
                self.finish_time = time.time()
            if self.number_of_files % CHECKPOINT_MULTIPLE == 0 or self.checkpoint_interval_elapsed() or finished:
                # once in a while, we do the update - because updating for every file would slow things down too much and not add
                # much greater accuracy
                file_ = open(self.temp_backup_id_filename, 'w')
                file_.write('start_time %f\n' % self.start_time)
                file_.write('number_of_files %d\n' % self.number_of_files)
                if finished:
                    # This means the backup finished well :)
                    file_.write('finish_time %f\n' % self.finish_time)
                else:
                    # If this is present in a backup_id long term, that indicates there was a crash of some sort that prevented the
                    # backup from completing normally.
                    file_.write('finish_time None\n')
                # make sure the data gets committed to disk
                file_.flush()
                os.fsync(file_.fileno())
                file_.close()

                # We create a temporary and rename, because that reduces the window during which a backup id's data could be
                # lost due to a crash.
                backshift_os_mod.safe_rename(self.temp_backup_id_filename, self.backup_id_filename)
                self.last_checkpoint_time = time.time()
            if finished:
                self.finished = True
        else:
            raise AssertionError('update called on old saveset')

#    def __enter__(self):
#        return self
#
#    def __exit__(self, type_, value, traceback):
#        if value is None:
#            self.close()
#            return True
#        else:
#            return False

    def close(self):
        """Close the saveset."""
        if self.new_saveset:
            self.update(finished=True)
            self.finish_time = time.time()
