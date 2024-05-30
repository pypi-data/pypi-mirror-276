#!/usr/bin/python

"""Manage a list of hardlinks for a given backup; Also provides classes for hardlink restores."""

# This is pretty good at dealing with 1,000,000,000 files, only 1,000 of which are hardlinks; this is
# probably the most common scenario for a backup program.
#
# It's also good at dealing with 1,000 distinct files, of which there are 1,000,000,000 each.
#
# It's not so good at dealing with 1,000,000,000 distinct files, each hardlinked to something else, for
# a total of 2,000,000,000 files.

import os
import collections

import dirops_mod
import bloom_filter_mod


def one():
    """Return 1, always - so our defaultdict can default to 1."""
    return 1


class Save_device(object):
    """Class to hold data related to a particular "device" on save - in unix/linux filesystems, this means a filesystem."""

    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods

    expected_size = None

    def __init__(self, deviceno):
        """Initialize."""
        self.deviceno = deviceno
        # This "bloom filter" will always correctly return True for something in the set, and will almost always
        # correctly return False for something not in the set.  It can infrequently return True for something
        # not in the set - so we maintain counts and deal with them later - but only for things that the filter
        # said was duplicated.  In this way, our inode_count defaultdict doesn't balloon up with a huge number
        # of 1's; the bloom filter is far smaller than that.
        self.bloom_filter = bloom_filter_mod.Bloom_filter(ideal_num_elements_n=Save_device.expected_size, error_rate_p=0.01)
        # This defaultdict defaults to one, because we only put things in it there are already in the
        # bloom filter (set).
        self.inode_count = collections.defaultdict(one)

    def __iadd__(self, inodeno):
        """Add an inode number to the list."""
        if inodeno in self.bloom_filter:
            self.inode_count[inodeno] += 1
        else:
            self.bloom_filter += inodeno
        return self

    def write(self, file_):
        """Write the list of duplicate inodes for this device."""
        for inodeno in self.inode_count:
            if self.inode_count[inodeno] > 1:
                file_.write('%d %d\n' % (inodeno, self.inode_count[inodeno]))


class Save_hardlinks(object):
    """Create a collection of duplicate inodes within the devices (filesystems) in which they appear."""

    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods

    backup_id = None

    def __init__(self, backup_id, expected_size):
        """Initialize."""
        if Save_hardlinks.backup_id is None:
            Save_hardlinks.backup_id = backup_id
        else:
            if Save_hardlinks.backup_id != backup_id:
                raise ValueError('Save_hardlinks.backup_id: %s, backup_id: %s' % (Save_hardlinks.backup_id, backup_id))
        self.device_dict = {}
        Save_device.expected_size = expected_size

    def __iadd__(self, tuple_):
        """Add a device number and inode number to the collection."""
        deviceno, inodeno = tuple_
        if not inodeno:
            # If inodeno is 0, we're probably on Windows, where inode numbers are always 0.
            # We should not treat a filesystem full of inode #0 as being 100% hardlinks.
            # So return without saving anything.
            # Note that, on a given machine, we could have one filesystem that inode numbers, and another that does not.
            return self
        if deviceno not in self.device_dict:
            self.device_dict[deviceno] = Save_device(deviceno)
        self.device_dict[deviceno] += inodeno
        return self

    def close(self):
        """Write the device # and inode # data we've collected."""
        directory = os.path.join('hardlinks', Save_hardlinks.backup_id)
        dirops_mod.my_mkdir(directory)
        for deviceno in self.device_dict:
            filename = os.path.join(directory, str(deviceno))
            file_ = open(filename, 'w')
            self.device_dict[deviceno].write(file_)
            file_.close()


class Restore_inode(object):
    """Class to hold inode data."""

    def __init__(self, inodeno, ideal_count):
        """Initialize."""
        self._ideal_count = ideal_count
        self._actual_count = 0
        self._inodeno = inodeno
        self._filename = None

    def get_filename(self):
        """Return the single filename associated with the first occurrence of this device+inode pair."""
        self._actual_count += 1
        return self._filename

    def set_filename(self, filename):
        """Associate a single filename with the first occurrence of this device+inode pair."""
        self._filename = filename


class Restore_hardlinks(object):
    """A class for dealing with restoration of hardlinks."""

    # pylint: disable=R0903
    # R0903: We don't need a lot of public methods

    backup_id = None

    def __init__(self, backup_id):
        """Initialize."""
        if Restore_hardlinks.backup_id is None:
            Restore_hardlinks.backup_id = backup_id
        else:
            raise ValueError('Restore_hardlinks: %s, backup_id: %s' % (Restore_hardlinks.backup_id, backup_id))
        self.device_dict = {}

        # Slurp in the hardlink-related data we created during the backup
        hardlinks_path = os.path.join('hardlinks', Restore_hardlinks.backup_id)
        for deviceno_string in os.listdir(hardlinks_path):
            deviceno = int(os.path.basename(deviceno_string))
            deviceno_path = os.path.join(hardlinks_path, deviceno_string)
            self.device_dict[deviceno] = {}
            file_ = open(deviceno_path, 'r')
            for line in file_:
                fields = line.split()
                inodeno = int(fields[0])
                count = int(fields[1])
                assert not fields[2:]
                self.device_dict[deviceno][inodeno] = Restore_inode(inodeno, count)
            file_.close()

    def prior_file_for_hardlink(self, deviceno, inodeno, filename):
        """
        Try to find a prior file for a hardlink.

        If this isn't a hardlinked file (in the backup), return None.
        If this is a hardlinked file, but it's the first time we've encountered the inode, save the filename and return None.
        If this is a hardlinked file, and we've seen the inode number previously, return the filename to which we should hardlink.
        """
        if deviceno not in self.device_dict:
            self.device_dict[deviceno] = {}

        if inodeno in self.device_dict[deviceno]:
            prior_filename = self.device_dict[deviceno][inodeno].get_filename()
            if prior_filename:
                assert prior_filename is not None
                return prior_filename
            self.device_dict[deviceno][inodeno].set_filename(filename)
            # This isn't a hardlink, because this is the first time we've encountered this inode number during
            # this restore.  However, a subsequent use of the inode number may be.
            return None
        else:
            # This isn't a hardlink, because the inode number isn't even in our table
            return None
