# -*- coding: utf-8 -*-

"""Class representing a explicit comments (@comment) in a bibtex file."""

from bibpy.entry import base


class Comment(base.BaseEntry):
    """Represents an explicit comment in a bibtex file."""

    def __init__(self, value):
        """Create a comment entry with a single value."""
        self._value = value

    def format(self, indent='    ', singleline=True, braces=True):
        """Format an return the comment entry as a string.

        If 'singleline' is True, put the entry on a single line
        If 'braces' is True, surround the entry by braces, else parentheses

        """
        return "@comment{0}{1}{2}{3}{4}"\
            .format('{' if braces else '(',
                    "" if singleline else "\n" + indent,
                    self.value,
                    "" if singleline else "\n",
                    '}' if braces else ')')

    @property
    def entry_type(self):
        """Return the entry type of this entry."""
        return 'comment'

    @property
    def entry_key(self):
        return None

    @property
    def fields(self):
        return []

    @property
    def value(self):
        """Return the value of the variable of the preamble."""
        return self._value

    def aliases(self, format):
        return []

    def valid(self, format):
        """Return True if all required fields are present, False otherwise."""
        # Comment entries only exist in bibtex
        return format == 'bibtex'

    def __eq__(self, other):
        return isinstance(other, Comment) and self.value == other.value

    def __contains__(self, item):
        """Check if an item is in the comment text."""
        return item in self.value

    def __getitem__(self, field):
        raise AttributeError(field)

    def __iter__(self):
        yield (None, self.value)

    def __len__(self):
        # There is only ever one value in a comment: Its contents
        return 1

    def __repr__(self):
        return "Comment(value=\"{0}\")".format(self.value)
