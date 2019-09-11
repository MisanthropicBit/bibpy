# -*- coding: utf-8 -*-

"""Class for names split into its components (given name, family name etc.)."""

import bibpy.compat
import bibpy.lexers
import sys

__all__ = frozenset(['Name'])


@bibpy.compat.unicode_compatibility
class Name(object):
    """Class containing the individual components of a name."""

    _lexer = bibpy.lexers.NameLexer()

    def __init__(self, first='', prefix='', last='', suffix=''):
        """Create a name consisting of first, prefix, last and suffix parts."""
        self._first = first
        self._prefix = prefix
        self._last = last
        self._suffix = suffix

    @classmethod
    def fromstring(_, string):
        """Extract the name parts of a string name."""
        return bibpy.parser.parse_name(string)

    @property
    def first(self):
        """Return the first or given name."""
        return self._first

    @property
    def given(self):
        """Alias for self.first."""
        return self.first

    @property
    def prefix(self):
        """Return the prefix (e.g. 'von')."""
        return self._prefix

    @property
    def von(self):
        """Alias for self.prefix."""
        return self.prefix

    @property
    def last(self):
        """Return the last or family name."""
        return self._last

    @property
    def family(self):
        """Alias for self.last."""
        return self.last

    @property
    def suffix(self):
        """Return the suffix (e.g. 'Jr.')."""
        return self._suffix

    @property
    def junior(self):
        """Alias for self.suffix."""
        return self.suffix

    @property
    def parts(self):
        """Return a tuple of all the name parts of this Name."""
        return (self.first, self.prefix, self.last, self.suffix)

    def _initials(self, s):
        """Return the initials for a name part.

        E.g. "Jane Gustav" => "J. G."

        """
        return ' '.join(e[0] + '.' for e in s.split())

    # NOTE: Support '{ff }{vv }{ll}{, jj}' syntax?
    # E.g. '{ff }{vv }{ll}{, jj}' => 'John von der Doe, Jr.'
    def format(self, style='first-last', initials=False):
        """Format the name using different styles. Default is 'first-last'.

        Consider the name 'John Smith' and its different styled formatings:
            * first-last => 'John Smith'
            * last-first => 'Smith, John'

        """
        if style == 'first-last':
            first = self._initials(self.first) if initials else self.first

            return ' '.join([first] + [p for p in self.parts[1:] if p])
        elif style == 'last-first':
            result = self.prefix if self.prefix else ''
            result += (' ' if self.prefix else '') + self.last
            result += ', ' + self.suffix if self.suffix else ''

            if self.first and (self.prefix or self.last):
                first = self._initials(self.first) if initials else self.first
                result += ', ' + first

            return result
        else:
            raise ValueError("Unrecognised style '{0}'".format(style))

    def __len__(self):
        """Return the number of name parts that this Name consists of."""
        return sum(1 for p in self.parts if p)

    def __eq__(self, other):
        if not isinstance(other, Name):
            return False

        return self.parts == other.parts

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.format()

    def __repr__(self):
        fmt = 'Name(first={0}, prefix={1}, last={2}, suffix={3})'

        # repr(x) is expected to return a byte-string in python 2 but a unicode
        # string in python 3
        if sys.version_info[0] > 2:
            return fmt.format(*self.parts)
        else:
            return fmt.format(*[p.encode('utf-8') for p in self.parts])
