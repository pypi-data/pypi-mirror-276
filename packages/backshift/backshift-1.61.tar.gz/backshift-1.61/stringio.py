#!/usr/bin/env python

"""Import a StringIO class on 2.x, or a BytesIO class on 3.x."""

try:
    # python 2 - fast way
    from cStringIO import StringIO
except ImportError:
    try:
        # python 2 - slow way
        from StringIO import StringIO
    except ImportError:
        # python 3
        from io import BytesIO as StringIO

_ = StringIO
