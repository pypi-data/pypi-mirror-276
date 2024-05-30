
# This file is intentionally not pylint'd, because it uses (formerly used) a bunch of different-but-similar modules, that are not
# all present in any single version of python.  BTW, I usually avoid "import * from", but in this case...  Apparently I have to
# make an exception.

# On pypy, dbm is typically a dbm-style interface to bsddb.
# gdbm_ctypes mostly works on pypy, but I suspect pypy of having a premature free() or similar in (tickled by?) its ctypes that
# prevents it being an effective solution for this application (1.4.1 and at least a couple of trunk snapshots thereafter).

# Rather than using different databases on different python's, I put together dohdbm.  It should be portable.

# try:
#    # python 3
#    from dbm.gnu import *
# except ImportError:
#    # python 2
#    try:
#        from gdbm_ctypes import *
#    except ImportError:
#        try:
#            from gdbm import *
#        except ImportError:
#            # this gets something that's kind of like bsddb on pypy 1.3 via ctypes
#            from dbm import *

"""Import some module that provides a key-value store."""

from dohdbm import open

_ = open
