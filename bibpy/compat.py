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
        return s.decode('utf-8', 'ignore')


def unicode_compatibility(cls):
    """Class decorator for Python 2/3 unicode compatibility.

    For this decorator to work, you must define __str__ on the class. For
    Python 2, it defines __str__ and __unicode__ whereas for Python 3 it does
    nothing.

    """
    if not __BIBPY_PY3__:
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda self: self.__unicode__().encode('utf-8')

    return cls
