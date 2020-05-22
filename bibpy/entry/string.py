# -*- coding: utf-8 -*-

"""Class representing a string entry in a bibtex file."""

from bibpy.entry.base import BaseEntry


class String(BaseEntry):
    """Represents a string entry in a bibtex file."""

    def __init__(self, variable, value):
        """Create an entry with a variable name and a value."""
        self._variable = variable.strip()
        self._value = value.strip()

    def format(self, indent='    ', singleline=True, braces=True, **kwargs):
        """Format an return the string entry as a string.

        If singleline is True, put the entry on a single line. The contents of
        the preamble is indented by the indent argument if singleline is True.

        If braces is True, surround the entry by braces, else parentheses.

        The kwargs are ignored for this entry type as there is no additional
        formatting.

        """
        contents = '{0} = "{1}"'.format(self.variable, self.value)

        return self.format_auxiliary_entry(
            'string',
            contents,
            indent,
            singleline,
            braces,
        )

    @property
    def bibtype(self):
        """Return the entry type of this entry."""
        return 'string'

    @property
    def bibkey(self):
        """Get the key (variable name) of this string entry."""
        return None

    @property
    def fields(self):
        """Return a dict of this entry's non-empty fields."""
        return [self.variable]

    @property
    def variable(self):
        """Return the variable name contained in the string entry."""
        return self._variable

    @variable.setter
    def variable(self, new_variable):
        self._variable = new_variable

    @property
    def value(self):
        """Return the value of the variable of this string entry."""
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def aliases(self, format):
        """Return any aliases of this entry."""
        return []

    def valid(self, format):
        """Return True if all required fields are present, False otherwise."""
        # String entries only exist in bibtex
        return format == 'bibtex'

    def __eq__(self, other):
        """Two string entries are equal if their variables and values match."""
        return isinstance(other, String)\
            and self.variable == other.variable\
            and self.value == other.value

    def __ne__(self, other):
        """Two string entries are equal if their variables and values match."""
        return not self == other

    def __contains__(self, item):
        """Check if an item is the variable of this string."""
        return item == self.variable

    def __getitem__(self, field):
        """Return the value for the given field."""
        if field == self.variable:
            return self.value

        raise AttributeError(field)

    def __iter__(self):
        yield (self.variable, self.value)

    def __len__(self):
        """Return the number of variables in the entry."""
        # There is only ever one variable in a string entry
        return 1

    def __repr__(self):
        return "String({0} = \"{1}\")".format(self.variable, self.value)
