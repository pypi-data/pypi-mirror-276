
"""Package up backshift for Pypi."""

import os
import distutils.core

version = '1.62'


def unlinker(filename):
    """Delete a file. Do not error if there is a problem doing so."""
    try:
        os.unlink(filename)
    except (OSError, IOError):
        pass


# These two are symlinks to themselves; they confuse distutils, so we delete them for setup.py's benefit
unlinker('tests/57-symlinks/to-be-saved/a/b/1')
unlinker('tests/57-symlinks/to-be-saved/c/d/2')


distutils.core.setup(
    name='backshift',
    py_modules=[
        'backshift_file_mod',
        'backshift_os_mod',
        'base255',
        'bloom_filter_mod',
        'bufsock',
        'cacher_mod',
        'chunk_mod',
        'comma_mod',
        'compressed_file_mod',
        'compressed_string_mod',
        'constants_mod',
        'db_mod',
        'dirops_mod',
        'dohdbm',
        'escape_mod',
        'expire_mod',
        'file_count_mod',
        'get_chunk',
        'hardlinks_mod',
        'helpers',
        'main',
        'metadata_mod',
        'modunits',
        'readline0',
        'repo_mod',
        'saveset_files_mod',
        'saveset_summary_mod',
        'stringio',
        'touch',
        'xz_mod',
        'zst_mod',
        'zst_zstandard',
        ],
    version=version,
    description='Filesystem to filesystem backup (deduplicated, compressed)',
    long_description="""
Backshift is a filesystem to filesystem backup program, analogous to rsync --link-dest.

Compared to rsync, backshift deduplicates much better, and compresses files - rsync does not.

Backshift also allows easy removal of old backups, despite its strong deduplication and compression.

Files to back up are selected using something like 'find / -xdev -print0' and piping that to backshift.

Files are restored by piping to 'tar xfp'.

Metadata is partially compressed.  Each directory's metadata is compressed separately for easy
partial restores.

Content-based, variable length chunks are deduplicated - so simply inserting a byte at a random place in a large file
is not going to require backing up the entire file anew.

Backshift runs on CPython 3.x and Pypy3.  It may run on nuitka - backshift+nuitka has not been tested much.

On many modern systems, Backshift runs fastest on Pypy, but on some (older?) machines you may be better off with
CPython 3.x plus the Cython versions of treap and rolling_checksum_mod.

For pypy, simply install backshift with pip.  This should give you a pure-python version of backshift that pypy likes.
For CPython+Cython, first install backshift with pip just as you would for pypy.  Then additionally install pyx-treap
and rolling-checksum-pyx-mod with pip - for a speed boost.

Backshift is not as fast as rsync --link-dest; rsync does not have to do as much work to accomplish what it sets out
to do.  But if you are paying for your storage, backshift will probably be significantly cheaper.
""",
    author='Daniel Richard Stromberg',
    author_email='strombrg@gmail.com',
    url='http://stromberg.dnsalias.org/~strombrg/backshift/',
    platforms='Cross platform',
    license='GPL, MIT, UCI, Apache (all opensource)',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        ],
    install_requires=[
        'treap',
        'rolling-checksum-py-mod',
        'zstandard',
        ],
    scripts=[
        'backshift',
        'backshift-extracts',
        'backshift-one',
        'backshift-recent-backup-id',
        'backshift-verify-file',
        'backshift-verify-filesystem',
        'count',
        'sshfs-backup',
        'strip-components',
        ],
    )
