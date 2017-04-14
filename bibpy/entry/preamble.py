#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Class representing a preamble in a bibtex file."""

from bibpy.entry import base


class Preamble(base.BaseEntry):
    """Represents a preamble in a bibtex file."""

    def __init__(self, value):
        """Create a preamble with a single value."""
        self._value = value.strip()

    def format(self, indent='    ', singleline=True, braces=True, **kwargs):
        """Format an return the preamble as a string.

        If 'singleline' is True, put the entry on a single line
        If 'braces' is True, surround the entry by braces, else parentheses

        """
        return "@preamble{0}{1}{2}{3}{4}"\
            .format('{' if braces else '(',
                    "" if singleline else "\n" + indent,
                    self.value,
                    "" if singleline else "\n",
                    '}' if braces else ')')

    @property
    def entry_type(self):
        """Return the entry type of this entry."""
        return 'preamble'

    @property
    def entry_key(self):
        """Return the key of this entry."""
        return None

    @property
    def fields(self):
        """Return a list of this entry's active bib(la)tex fields.

        Active fields are fields that are not None or empty strings.

        """
        return []

    @property
    def value(self):
        """Return the value of the variable of the preamble."""
        return self._value

    def aliases(self, format):
        """Return any aliases of this entry."""
        return []

    def valid(self, format):
        """Return True if all required fields are present, False otherwise."""
        # Preamble entries only exist in bibtex
        return format == 'bibtex'

    def __eq__(self, other):
        return isinstance(other, Preamble) and self.value == other.value

    def __contains__(self, item):
        """Check if an item is in the preamble code."""
        return item in self.value

    def __getitem__(self, field):
        raise AttributeError(field)

    def __iter__(self):
        yield (None, self.value)

    def __len__(self):
        """Return the number of variables in the entry."""
        # There is only ever one variable in a preamble
        return 1

    def __repr__(self):
        return "Preamble(value=\"{0}\")".format(self.value)
