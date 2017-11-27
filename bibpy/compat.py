# -*- coding: utf-8 -*-

"""Compatibility functions for bibpy."""

import sys

__BIBPY_PY3__ = sys.version_info[0] > 2


def is_string(s):
    """Check if the argument is a string or not."""
    if __BIBPY_PY3__:
        return isinstance(s, str)
    else:
        return isinstance(s, basestring)


# Portable unicode string literals
if __BIBPY_PY3__:
    def u(s):
        return s
else:
    def u(s):
        return unicode(s)
