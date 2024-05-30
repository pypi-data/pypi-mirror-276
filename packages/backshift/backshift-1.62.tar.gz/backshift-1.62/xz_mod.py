#!/usr/bin/env python

# pylint: disable=W0404,F0401,simplifiable-if-statement,superfluous-parens
# W0404: pylint -thinks- we're reimporting ctypes.util, but we aren't really
# F0401: We can't always import lzma, but don't stress about that - it only exists in 3.3
# simplifiable-if-statement: We use module-level variables to tell us what's importing and what's not
# superfluous-parens: Parentheses are good for portability and clarity

"""Impersonate the real xz module, which has yet to be written and/or added to CPython, by using the xz binary."""

import os
import tempfile
import subprocess

try:
    import ctypes
    import ctypes.util
except ImportError:
    HAVE_CTYPES = False
else:
    HAVE_CTYPES = True

try:
    import lzma
except ImportError:
    try:
        # Sometimes Pypy 2.x will have this, perhaps CPython too.  It's a CFFI lzma module.
        import lzmaffi as lzma
    except ImportError:
        HAVE_LZMA = False
    else:
        HAVE_LZMA = True
else:
    HAVE_LZMA = True


class DecompressionError(Exception):
    """An exception to raise if there is a problem decompressing data.  Should be rare but not nonexistent in practice."""

    # Currently only used by MEANS = 'lzma module'
    pass


if hasattr(os, 'uname'):
    FUNCTION = getattr(os, 'uname')
    UNAME = FUNCTION()[0]
else:
    # This is probably Jython, but Unknown is good enough for now, and more likely to be accurate in the future
    # as the code adapts to new requirements.  We really only care about Cygwin for now, and that has an os.uname().
    UNAME = 'Unknown'

# This module does the same thing: compression/decompression, in two different ways:
# 1) The normal way, via the subprocess module (which has problems sometimes on Cygwin, because Cygwin merely
#    emulates fork, and does so a bit poorly: Read "slowly, and unreliably".  This variant uses no temporary
#    files.
# 2) Via os.popen, which has fallen into disfavor, but seems to work better on Windows.  This variant uses
#    one temporary file for every compress, and one temporary file for every decompress.

# Other possibilities:
# 3) Use the multiprocessing module - that purporetedly works fine on Windows, but it isn't included in Python
#    until 2.6
# 4) Write a ctypes-based module - this chances having problens on PyPy, given my experience with gdbm_ctypes
# 5) Use a cython module - again, PyPy issues
# 6) Use a C extension module - again, PyPy issues

# Note that neither the generic version of the Cygwin version is especially fast in this version of xz_mod, though
# the generic version is faster than the Cygwin version.


def find_xz():
    """Find the xz binary, if any."""
    path = os.environ['PATH']
    directories = path.split(':')
    for directory in directories:
        candidate_executable = os.path.join(directory, 'xz')
        if os.access(candidate_executable, os.X_OK):
            return candidate_executable
    return None


def _find_lib(library):
    """Find our libraries, one at a time."""
    normal_result = ctypes.util.find_library(library)
    if normal_result is None:
        # find_library doesn't appear to be able to find cygwin DLL's, so
        # we have extra code to help with that - in part because fork+exec
        # is very slow on windows, so we really want the ctypes version
        # of xz there.
        for dll_vers in range(11, 1, -1):
            candidate_filename = '/bin/cyg%s-%d.dll' % (library, dll_vers)
            if os.path.isfile(candidate_filename):
                return candidate_filename

        # This is for Haiku
        for so_vers in range(11, 1, -1):
            candidate_filename = '/boot/common/lib/lib%s.so.%s' % (library, so_vers)
            print('checking %s' % (candidate_filename,))
            if os.path.isfile(candidate_filename):
                return candidate_filename

        # Didn't find library
        return None
    return normal_result


XZ_PATH = find_xz()


class Xz_ctypes(object):
    """A class to compress and decompress xz format, using ctypes to access liblzma."""

    LZMA_OK = 0
    LZMA_TELL_NO_CHECK = 1
    LZMA_CHECK_CRC32 = 1
    LZMA_NO_CHECK = 2
    LZMA_TELL_UNSUPPORTED_CHECK = 2
    LZMA_UNSUPPORTED_CHECK = 3
    LZMA_MEM_ERROR = 5
    LZMA_MEMLIMIT_ERROR = 6
    LZMA_PRESET_DEFAULT = 6
    LZMA_FORMAT_ERROR = 7
    LZMA_OPTIONS_ERROR = 8
    LZMA_DATA_ERROR = 9
    LZMA_BUF_ERROR = 10
    LZMA_PROG_ERROR = 11
    long_message = 'LZMA_MEMLIMIT_ERROR: Memory usage limit was reached.  ' + \
        'minimum required memlimit value was stored to *memlimit'

    long_string = "LZMA_FORMAT_ERROR: Magic bytes don't match, thus the given buffer cannot be Stream Header."
    error_dict = {
        LZMA_PRESET_DEFAULT:            'LZMA_PRESET_DEFAULT',
        LZMA_CHECK_CRC32:               'LZMA_CHECK_CRC32',
        LZMA_OK:                        'LZMA_OK',
        LZMA_FORMAT_ERROR:              long_string,
        LZMA_OPTIONS_ERROR:             'LZMA_OPTIONS_ERROR',
        LZMA_DATA_ERROR:                'LZMA_DATA_ERROR',
        LZMA_NO_CHECK:                  'LZMA_NO_CHECK',
        LZMA_TELL_NO_CHECK:             'LZMA_TELL_NO_CHECK',
        LZMA_UNSUPPORTED_CHECK:         'LZMA_UNSUPPORTED_CHECK',
        LZMA_TELL_UNSUPPORTED_CHECK:    'LZMA_TELL_UNSUPPORTED_CHECK',
        LZMA_MEM_ERROR:                 'LZMA_MEM_ERROR',
        LZMA_MEMLIMIT_ERROR:            long_message,
        LZMA_BUF_ERROR:                 'LZMA_BUF_ERROR: Output buffer was too small',
        LZMA_PROG_ERROR:                'LZMA_PROG_ERROR',
    }

    funcs = {}

    def __init__(self):
        """Initialize."""
        pass

    @classmethod
    def declare_c_function(cls, library, name, argtypes=None, restype=None):
        """Extract functions from liblzma."""
        try:
            func = getattr(library, '_%s' % name)
            cls.funcs[name] = func
        except AttributeError:
            func = getattr(library, name)
            cls.funcs[name] = func
        if argtypes is not None:
            func.argtypes = argtypes
        if restype is not None:
            func.restype = restype

    @classmethod
    def class_init(cls):
        """Initialize the class."""
        cls.LZMA_LIBPATH = _find_lib('lzma')

        if cls.LZMA_LIBPATH is None:
            raise ImportError('Could not find lzma library')

        # *ix way - windows is different
        cls.LZMA_LIB = ctypes.CDLL(cls.LZMA_LIBPATH)

        cls.declare_c_function(
            cls.LZMA_LIB,
            'lzma_stream_buffer_bound',
            (ctypes.c_size_t, ),
            ctypes.c_size_t,
        )

        # lzma_easy_buffer_encode notes:
        # Argument 1, uint32_t preset:
        #    Just a uint32 - simple
        # Argument 2, lzma_check check:
        #    An enum to the C programmer - that should usually be an unsigned integer in the C runtime.
        # Argument 3, lzma_allocator *lzma_allocator:
        #    This is really a pointer to a struct, but happily, we only need to pass NULL to it,
        #    so we can just treat it as a void *
        # Argument 4: uint8_t *in:
        # Argument 5: size_t in_size:
        # Argument 6: uint8_t *out
        # Argument 7: size_t *out_pos
        # Argument 8: size_t out_size
        #
        # The return type is also an enum, so probably an unsigned int
        cls.declare_c_function(
            cls.LZMA_LIB,
            'lzma_easy_buffer_encode', (
                ctypes.c_uint32,                    # preset
                ctypes.c_uint,                      # check
                ctypes.c_void_p,                    # lzma_allocator
                ctypes.POINTER(ctypes.c_uint8),     # uint8_t *in
                ctypes.c_size_t,                    # size_t in_size
                ctypes.POINTER(ctypes.c_uint8),     # uint8_t *out
                ctypes.POINTER(ctypes.c_size_t),    # size_t *out_pos
                ctypes.c_size_t,                    # size_t out_size
            ),
            ctypes.c_uint,
        )

        cls.declare_c_function(
            cls.LZMA_LIB,
            'lzma_stream_buffer_decode', (
                ctypes.POINTER(ctypes.c_uint64),    # uint64_t *memlimit
                ctypes.c_uint32,                    # uint32_t flags
                ctypes.c_void_p,                    # lzma_allocator *allocator,
                ctypes.POINTER(ctypes.c_uint8),     # const uint8_t *in
                ctypes.POINTER(ctypes.c_size_t),    # size_t *in_pos
                ctypes.c_size_t,                    # size_t in_size,
                ctypes.POINTER(ctypes.c_uint8),     # uint8_t *out
                ctypes.POINTER(ctypes.c_size_t),    # size_t *out_pos
                ctypes.c_size_t,                    # size_t out_size
            ),
            ctypes.c_uint,
        )

    @classmethod
    def get_xz_error(cls, ret_xz):
        """Decode an lzma_ret enum to an at-least-somewhat-descriptive string."""
        if ret_xz in cls.error_dict:
            return cls.error_dict[ret_xz]
        return 'Unrecognized lzma_ret value: %d' % ret_xz

    @classmethod
    def compress(cls, input_data):
        """Compress data into xz format using ctypes to access liblzma.so."""
        # maximum_size = lzma_stream_buffer_bound(input_buffer_size);
        length_input_data = len(input_data)
        maximum_size = cls.funcs['lzma_stream_buffer_bound'](length_input_data)

        # This is an efficient way of creating a readonly ctypes string
        ctypes_input_data_char_p = ctypes.c_char_p(input_data)
        ctypes_input_data = ctypes.cast(ctypes_input_data_char_p, ctypes.POINTER(ctypes.c_ubyte))

        # Here is a less-fast but mutable way of creating a ctypes string.
        # This works most of the time, but pypy2 5.10.0 has problems with it:
        # ctypes_compressed_buffer_char_p = ctypes.create_string_buffer(maximum_size)
        # This is a viable alternative:
        ctypes_compressed_buffer_char_p = ctypes.create_string_buffer(b'\0' * maximum_size)
        ctypes_compressed_buffer = ctypes.cast(ctypes_compressed_buffer_char_p, ctypes.POINTER(ctypes.c_ubyte))

        ctypes_compressed_size = ctypes.c_size_t(0)
        ctypes_compressed_size_pointer = ctypes.cast(ctypes.addressof(ctypes_compressed_size), ctypes.POINTER(ctypes.c_size_t))

        # lzma_easy_buffer_encode
        ret_xz = cls.funcs['lzma_easy_buffer_encode'](
            cls.LZMA_PRESET_DEFAULT,
            cls.LZMA_CHECK_CRC32,
            None,
            ctypes_input_data,
            length_input_data,
            ctypes_compressed_buffer,
            ctypes_compressed_size_pointer,
            maximum_size,
        )

        if ret_xz != cls.LZMA_OK:
            raise OSError(cls.get_xz_error(ret_xz))

        resultant_length = int(ctypes_compressed_size.value)
        result = ctypes_compressed_buffer_char_p.raw[:resultant_length]

        return result

    @classmethod
    def decompress(cls, input_data, max_result_size=2 ** 26):
        # pylint: disable=R0914
        # R0914: We need some locals for this one
        """Uncompress data from xz format using ctypes to access liblzma.so."""
        ctypes_memlimit = ctypes.c_uint64(max_result_size)
        ctypes_memlimit_pointer = ctypes.cast(ctypes.addressof(ctypes_memlimit), ctypes.POINTER(ctypes.c_uint64))

        ctypes_input_data_char_p = ctypes.c_char_p(input_data)
        ctypes_input_data = ctypes.cast(ctypes_input_data_char_p, ctypes.POINTER(ctypes.c_ubyte))

        ctypes_in_pos = ctypes.c_size_t(0)
        ctypes_in_pos_pointer = ctypes.cast(ctypes.addressof(ctypes_in_pos), ctypes.POINTER(ctypes.c_size_t))

        in_size = ctypes.c_size_t(len(input_data))

        ctypes_uncomp_buffer_char_p = ctypes.create_string_buffer(max_result_size)
        ctypes_uncompressed_buffer = ctypes.cast(ctypes_uncomp_buffer_char_p, ctypes.POINTER(ctypes.c_ubyte))

        ctypes_out_pos = ctypes.c_size_t(0)
        ctypes_out_pos_pointer = ctypes.cast(ctypes.addressof(ctypes_out_pos), ctypes.POINTER(ctypes.c_size_t))

        out_size = ctypes.c_size_t(max_result_size)

        ret_xz = cls.funcs['lzma_stream_buffer_decode'](
            ctypes_memlimit_pointer,            # uint64_t *memlimit
            cls.LZMA_TELL_NO_CHECK,             # uint32_t flags
            None,                               # lzma_allocator *allocator,
            ctypes_input_data,                  # const uint8_t *in
            ctypes_in_pos_pointer,              # size_t *in_pos
            in_size,                            # size_t in_size,
            ctypes_uncompressed_buffer,         # uint8_t *out
            ctypes_out_pos_pointer,             # size_t *out_pos
            out_size,                           # size_t out_size
        )

        if ret_xz != cls.LZMA_OK:
            raise OSError(cls.get_xz_error(ret_xz))

        resultant_length = int(ctypes_out_pos.value)
        result = ctypes_uncomp_buffer_char_p.raw[:resultant_length]

        return result


if HAVE_CTYPES:
    XZ_CTYPES = Xz_ctypes()
    XZ_CTYPES.class_init()


def use_lzma():
    """Return True if we should use the lzma module."""
    if HAVE_LZMA and hasattr(lzma, 'FORMAT_XZ'):
        return True
    return False


def use_ctypes():
    """Return True if we should use the ctypes version."""
    if HAVE_CTYPES and _find_lib('lzma') is not None:
        return True
    return False


def use_popen():
    """Return True if we should use the popen version."""
    if UNAME.startswith('CYGWIN'):
        return True
    return False


def use_subprocess():
    """Return True if we should use the subprocess module."""
    if XZ_PATH is not None:
        return True
    return False


if use_lzma():

    MEANS = 'lzma module'

    def compress(data):
        # pylint: disable=no-member
        # Some python's don't have these
        """Compress a block of data using lzma/xz."""
        return lzma.compress(data, format=lzma.FORMAT_XZ, preset=lzma.PRESET_DEFAULT, check=lzma.CHECK_CRC32)

    def decompress(data):
        # pylint: disable=no-member
        # Some python's don't have these
        """Decompress a block of data using lzma/xz."""
        try:
            return lzma.decompress(data, format=lzma.FORMAT_XZ)
        except lzma.LZMAError:
            raise DecompressionError
elif use_popen():

    MEANS = 'Windows popen'

    def compress(data):
        """Compress data using an xz executable and the popen function (to avoid fork on Windows).  Uses temporary files."""
        if XZ_PATH is None:
            raise OSError('xz not found')

        args = {}
        args['mode'] = 'w+b'
        args['suffix'] = '.backshifttemp'
        args['prefix'] = 'tmp'
        args['delete'] = False
        temp_file = tempfile.NamedTemporaryFile(**args)
        temp_filename = temp_file.name
        temp_file.write(data)
        temp_file.close()

        pipe = os.popen('%s -z < %s' % (XZ_PATH, temp_filename), 'rb')
        result = pipe.read()
        retval = pipe.close()
        if retval is None:
            retval = 0
        exit_code = retval / 256
        if exit_code:
            raise OSError('compress failed')

        os.unlink(temp_filename)

        return result

    def decompress(data):
        """Decompress data using an xz executable and the popen function (to avoid fork on Windows).  Uses temporary files."""
        if XZ_PATH is None:
            raise OSError('xz not found')

        args = {}
        args['mode'] = 'w+b'
        args['suffix'] = '.backshiftemp'
        args['prefix'] = 'tmp'
        args['delete'] = False
        temp_file = tempfile.NamedTemporaryFile(**args)
        temp_filename = temp_file.name
        temp_file.write(data)
        temp_file.close()

        pipe = os.popen('%s -d < %s' % (XZ_PATH, temp_filename), 'rb')
        result = pipe.read()
        retval = pipe.close()
        if retval is None:
            retval = 0
        exit_code = retval / 256
        if exit_code:
            raise OSError('decompress failed')

        os.unlink(temp_filename)

        return result

elif use_ctypes():

    MEANS = 'ctypes'

    def compress(data):
        """Compress using ctypes - just hand off to XZ_CTYPES."""
        return XZ_CTYPES.compress(data)

    def decompress(data):
        """Decompress using ctypes - just hand off to XZ_CTYPES."""
        return XZ_CTYPES.decompress(data)

elif use_subprocess():

    MEANS = 'xz subprocess'

    def compress(data):
        # pylint: disable=E1101
        # E1101: actually Popen objects do have a returncode member
        """Compress data using an xz executable and the subprocess module."""
        if XZ_PATH is None:
            raise OSError('xz not found')

        subp = subprocess.Popen([XZ_PATH, "-z"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = subp.communicate(input=data)
        if subp.returncode != 0:
            raise OSError('Chunk failed to compress: %s' % stderr)
        return stdout

    def decompress(data):
        # pylint: disable=E1101
        # E1101: actually Popen objects do have a returncode member
        """Decompress data using an xz executable and the subprocess module."""
        if XZ_PATH is None:
            raise OSError('xz not found')

        subp = subprocess.Popen([XZ_PATH, "-d"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = subp.communicate(input=data)
        if subp.returncode != 0:
            raise OSError('Chunk failed to decompress: %s' % stderr)
        return stdout
else:
    raise ValueError('No suitable form of xz compression found')
