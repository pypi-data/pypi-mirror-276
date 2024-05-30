#!/usr/bin/env python

# pylint: disable=simplifiable-if-statement
# simplifiable-if-statement

"""Provides a Cacher class, for caching database tables from gdbm files."""

# mport sys
import time
# mport pprint
# mport traceback

import treap
import db_mod
# mport decimal


class Database_cacher_error(Exception):
    # pylint: disable=W0232
    # W0232: We don't need an __init__ method
    """A generic exception for cacher errors."""

    pass


class Database_cacher_duplicate_error(Database_cacher_error):
    # pylint: disable=W0232
    # W0232: We don't need an __init__ method
    """An exception for when we have a duplicate filename."""

    pass


class Database_cacher_time_error(Database_cacher_error):
    # pylint: disable=W0232
    # W0232: We don't need an __init__ method
    """An exception for when we have a timing problem."""

    pass


class Database_cacher(object):
    """
    A Database Cache class, for caching database tables from key-value stores.

    The cache is LRU: We evict the Least Recently Used table when we need more room.
    """

    # We store one entry in this for each directory backed up

    def __init__(self, max_entries):
        """Initialize."""
        self.filename_to_database_dict = {}
        self.time_to_filename_treap_list = treap.treap()
        self.filename_to_time_dict = {}
        self.max_entries = max_entries
        self.touchno = 0
        self.time_of_last_syncs = time.time()

    def _touch(self, filename):
        """
        Update (or create anew) the timestamps on this filename in the cache.

        This is done so the filename isn't evicted from the cache as soon.
        """
        # We update two collections:
        # 1) time_to_filename_treap_list
        # 2) filename_to_time_dict
        # We needn't do anything with filename_to_database_dict

        # We convert the time to decimal, because it isn't so subject to the whims of floating point comparison, and we rely
        # on comparisons being precise.  We use a strictly increasing "touchno" to deal with the possibility of the clock being
        # too granular to disambiguate fully.
        # current_time = (decimal.Decimal(str(time.time())), self.touchno)
        current_time = self.touchno
        self.touchno += 1

        # 1) Update filename_to_filename_treap_list
        # 1b) Remove any traces of previous entries, if they exist
        if filename in self.filename_to_time_dict:
            prior_time = self.filename_to_time_dict[filename]
            if prior_time in self.time_to_filename_treap_list:
                # first, remove the filename from its previous list, deleting the old list if it has become empty
                filenames_at_prior_time = self.time_to_filename_treap_list[prior_time]
                if filename in filenames_at_prior_time:
                    filenames_at_prior_time.remove(filename)
                    if not filenames_at_prior_time:
                        del self.time_to_filename_treap_list[prior_time]
                else:
                    raise Database_cacher_time_error("a")
            else:
                raise Database_cacher_time_error("b")

        # 1) Update filename_to_filename_treap_list (continued)
        # 1c) Add new entries
        if current_time in self.time_to_filename_treap_list:
            self.time_to_filename_treap_list[current_time].append(filename)
        else:
            # BTW, this will mostly be lists of a single element.  We want to allow duplicate times in case things
            # are moving along rapidly, but we don't want to require that all times be distinct.
            self.time_to_filename_treap_list[current_time] = [filename]

        # 2) Update filename_to_time_dict
        self.filename_to_time_dict[filename] = current_time

    def __len__(self):
        """Return the number of filenames in the dict."""
        return len(self.filename_to_database_dict)

    def __contains__(self, filename):
        """Return True iff the database contains 'filename'."""
        return filename in self.filename_to_database_dict

    def keys(self):
        """Give us a list of filenames in the cache."""
        return self.filename_to_database_dict.keys()

    def _possible_syncs(self):
        """Once every three hours: Iterate over the older part of the cache.  Call the database's sync method."""
        # one hour
        interval = 60 * 60 * 3
        current_time = time.time()
        if current_time > self.time_of_last_syncs + interval:
            self.time_of_last_syncs = current_time
            threshold_time = current_time - interval
            for database_touched_time in self.time_to_filename_treap_list.reverse_iterator():
                # We only bother with things that haven't been "touched" (read or written) via a Database_cacher method for over
                # an hour.  BTW, we know that the cache entries will come up in the above for loop in reverse chronological order,
                # orderbecause the treap is ordered and we're using a reverse iterator.
                if database_touched_time < threshold_time:
                    for filename in self.time_to_filename_treap_list[database_touched_time]:
                        database = self.filename_to_database_dict[filename]
                        try:
                            # This will raise some random exception (depending on the database module in use) if the database
                            # has been closed - this module doesn't see the closes.  So we catch and ignore any exception on
                            # the sync().
                            database.sync()
                        except db_mod.error:
                            pass
                else:
                    # So from here, all other entries in the cache have been used less recently than this one, hence they
                    # can be skipped.
                    return

    def __getitem__(self, filename):
        """Look up a filename in the cache."""
        if filename in self.filename_to_database_dict:
            self._touch(filename)
            self._possible_syncs()
            return self.filename_to_database_dict[filename]
        else:
            raise KeyError("Filename %s not in cacher instance" % filename)

    def __setitem__(self, filename, value):
        """Add a filename and its value to the cache."""
        if filename in self.filename_to_database_dict:
            raise Database_cacher_duplicate_error
        self.filename_to_database_dict[filename] = value
        self._touch(filename)
        self._possible_syncs()
        self.expire_down_to()

    def expire_down_to(self, down_to=None):
        """Expire entries from the cache until we have < down_to entries."""
        if down_to is None:
            down_to = self.max_entries

        while len(self.filename_to_database_dict) > down_to:
            # First we remove from time_to_filename_treap_list
            least_time = self.time_to_filename_treap_list.find_min()
            least_time_filename_list = self.time_to_filename_treap_list[least_time]
            if least_time_filename_list[1:]:
                # there's more than one filename at this time; remove one
                least_filename = least_time_filename_list.pop()
                # We had a reference to what's still inside the treap, so the treap has been updated
            else:
                least_filename = least_time_filename_list[0]
                del self.time_to_filename_treap_list[least_time]

            # next we remove from filename_to_time_dict
            del self.filename_to_time_dict[least_filename]

            # and finally we remove from filename_to_database_dict
            self.filename_to_database_dict[least_filename].close()

            del self.filename_to_database_dict[least_filename]

    def expire_all(self):
        """Expire all entries from the cache."""
        # There's an O(n) way of doing this, but for now, we do it in O(n*log(n)) time for accuracy and speed of coding
        self.expire_down_to(down_to=0)

    close = expire_all

#    def __enter__(self):
#        return self
#
#    def __exit__(self, type_, value, traceback_):
#        if value is None:
#            self.expire_all()
#            return True
#        else:
#            return False
