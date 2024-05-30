#!/usr/local/pypy3-7.3.3/bin/pypy3


"""Performance comparison between difference methods of doing 'touch' in Python."""

import functools
import os
from pathlib import Path
import sys
import timeit


def touch1(filename):
    """Touch a file using pathlib - fastest on pypy3, and fastest overall - but has problems with non-UTF-8 filenames."""
    Path(filename).touch()


def touch2(filename):
    """Touch a file using open+close."""
    open(filename, 'r+').close()


def touch3(filename, flags=os.O_CREAT | os.O_RDWR):
    """Touch a file using os.open+os.close - fastest on CPython 3.11."""
    os.close(os.open(filename, flags, 0o644))


def touch4(filename):
    """Touch a file using open+close."""
    open(filename, 'a').close()


def make_used(*variables):
    """Persuade linters that 'variables' are used."""
    assert True or variables


def create_test_file(filename, size):
    """Create a test file at filename of size bytes."""
    with open(filename, 'w') as file_:
        file_.write('0' * size)


if sys.implementation.name == 'pypy':
    # Second-fastest on Pypy, but works for all filenames, not just UTF-8 names.
    touch = touch3
elif sys.implementation.name == 'cpython':
    touch = touch3
else:
    print('This does not appear to be pypy or cpython - using an unoptimized touch', file=sys.stderr)
    touch = touch4


@functools.total_ordering
class Result:
    """Hold one performance result."""

    def __init__(self, time, fn):
        """Initialize."""
        self.time = time
        self.fn = fn

    def __lt__(self, other):
        """Less than."""
        return self.time < other.time

    def __eq__(self, other):
        """Equal."""
        return self.time == other.time


def main():
    """Start the performance test."""
    filename = 'megs-of-data.txt'
    size = 2**25
    create_test_file(filename, size)
    assert os.path.getsize(filename) == size
    make_used(filename)
    results = []
    for fn in (touch1, touch2, touch3, touch4):
        print(fn)
        time = timeit.timeit(functools.partial(fn, filename), number=10_000_000)
        assert os.path.getsize(filename) == size
        print(time)
        print()
        results.append(Result(time, fn))

    best = min(results)

    print('On your {} {}.{}.{} {} is fastest'.format(
        sys.implementation.name,
        sys.implementation.version.major,
        sys.implementation.version.minor,
        sys.implementation.version.micro,
        best.fn,
    ))

    if best.fn == touch:
        print('That is expected, no tuning needed')
    else:
        print('That was unexpected, please tune touch.py accordingly')


if __name__ == '__main__':
    main()
