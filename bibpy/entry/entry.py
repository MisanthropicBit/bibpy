# -*- coding: utf-8 -*-

"""Class representing single entries in a bib file."""

from bibpy.entry.base import BaseEntry
from bibpy.preprocess import preprocess
import bibpy.entries
import bibpy.error
import bibpy.fields
import bibpy.requirements
import collections
from collections.abc import Iterable
import itertools


class Entry(BaseEntry):
    """Represents an entry in a bib file."""

    # List of predefined properties that cannot be set through setattr etc.
    _locked_fields = frozenset([
        'bibkey',
        'bibtype',
        'fields',
        'extra_fields',
        'aliases',
        'valid',
        'validate',
        'keys',
        'values',
        'clear'
    ])

    def __init__(self, bibtype='', bibkey='', fields=(), **kw_fields):
        """Create a bib entry with a type, key and fields.

        Pass an iterable of name/value pairs denoting fields to keep the order.

        Using keyword arguments are not guaranteed to keep the same ordering
        until Python 3.6 (see PEP 468).

        """
        # We use an ordered dict here to maintain the same order as the fields
        # are listed in files
        self._fields = collections.OrderedDict()
        self._bibtype = bibtype
        self._bibkey = bibkey

        for field, value in itertools.chain(fields, kw_fields.items()):
            setattr(self, field, value)

    def format(self, align=True, indent='    ', order=[], surround='{}',
               **kwargs):
        """Format and return the entry as a string.

        If align is True, align the equal signs of all fields.

        The indent is a string that controls the type of indentation before a
        field.

        The order is a either bool that sorts alphabetically if True, or a list
        of the order of a subset of fields, e.g. ['author', 'title'] would
        place those two fields in the given order before any other fields.

        Additional kwargs are formatting options passed on to the preprocessing
        function that converts Python types into bibliographic data for
        writing.

        """
        entry_start = '@' + self.bibtype + '{' + self.bibkey + ',\n'

        if not self.fields:
            return entry_start + '}'

        fields = []

        if order:
            if isinstance(order, bool):
                # Sort alphabetically
                fields = sorted(preprocess(self, self.fields, **kwargs))
            elif isinstance(order, Iterable) and not isinstance(order, str):
                # Sort according to the specified order
                order = [o for o in order if getattr(self, o, None)]
                ordered_fields = preprocess(self, order, **kwargs)
                other_fields = preprocess(
                    self,
                    [f for f in self.fields if f not in order],
                    **kwargs
                )

                fields = list(ordered_fields) + list(other_fields)

            else:
                raise ValueError(
                    "order must be either a bool-like or non-string iterable, "
                    "not '{0}'".format(type(order))
                )
        else:
            # Otherwise, just preprocess all fields in their current order
            for field, value in preprocess(self, self.fields, **kwargs):
                fields.append((field, value))

        mx = max(len(field) for field in self.fields)

        formatted_fields = [
            '{0}{1}{2} = {3}{4}{5}'.format(
                indent,
                field,
                (' ' * (mx - len(field)) if align else ''),
                surround[0], value, surround[1]
            ) for field, value in fields
        ]

        return entry_start + ',\n'.join(formatted_fields) + '\n}'

    @property
    def bibtype(self):
        """Return the entry type of this entry."""
        return self._bibtype

    @bibtype.setter
    def bibtype(self, value):
        self._bibtype = value

    @property
    def bibkey(self):
        """Return the key of this entry."""
        return self._bibkey

    @bibkey.setter
    def bibkey(self, value):
        self._bibkey = value

    @property
    def fields(self):
        """Return a list of active bib(la)tex fields.

        Active fields are fields that are not None or empty strings.

        """
        return list(self._fields)

    @property
    def extra_fields(self):
        """Return any extra fields not recognised as bibtex or biblatex.

        This also ignores user-defined attributes that begin with an
        underscore.

        """
        return [ef for ef in self.fields if ef not in bibpy.fields.all]

    def get(self, name, default=None):
        """Return the value for name or default if the name does not exist."""
        return getattr(self, name, default)

    def aliases(self, format):
        """Return any aliases of this entry."""
        return bibpy.entries.aliases(self.bibtype, format)

    def valid(self, format):
        """Return True if all required fields are present, False otherwise."""
        required, optionals = bibpy.requirements.check(self, format)

        return not required and not optionals

    def validate(self, format):
        """Raise an error if required fields are missing for the format."""
        required, optionals = bibpy.requirements.check(self, format)

        if required or optionals:
            raise bibpy.error.RequiredFieldError(self, required, optionals)

    def keys(self):
        """Return a list of field names in the entry."""
        return self.fields

    def values(self):
        """Return a list of field values in the entry."""
        return [getattr(self, field) for field in self.fields]

    def clear(self):
        """Clear all the fields of this entry."""
        for field in self.fields:
            setattr(self, field, None)

    def __eq__(self, other):
        """Entries are equal if their types, keys, fields and values match."""
        if not isinstance(other, Entry):
            return False

        if self.bibtype != other.bibtype or self.bibkey != other.bibkey:
            return False

        if set(self.fields) == set(other.fields):
            for field in self.fields:
                if getattr(self, field) != getattr(other, field):
                    return False
        else:
            return False

        return True

    def __ne__(self, other):
        """Entries are not equal if their fields and values do not match."""
        return not self.__eq__(other)

    def __contains__(self, item):
        """Check if the active field is set for this entry.

        Does not check general attributes, only active fields.

        """
        return item in self.fields or item in self.extra_fields

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if not name.startswith('_') and name not in Entry._locked_fields:
            if value is None or value == '':
                if name in self._fields:
                    self._fields.pop(name)
            else:
                self._fields[name] = None

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, field):
        """Return the value for the given field."""
        return getattr(self, field, None)

    def __delitem__(self, key):
        """Delete a field and its value from the entry."""
        setattr(self, key, None)

    def __len__(self):
        """Return the number of fields and extra fields in this entry."""
        return len(self.fields)

    def __repr__(self):
        return "Entry(type={0}, key={1})".format(self.bibtype, self.bibkey)


def autoproperty(name, getter=True, setter=True, prefix='_', doc=''):
    """Autogenerate a property."""
    attribute = prefix + name

    def _getter(self):
        return getattr(self, attribute, None)

    def _setter(self, value):
        setattr(self, attribute, value)

    # Do not add a dot to multi-line docstrings
    if not ('\n' in doc or '\r\n' in doc) and not doc.endswith('.'):
        doc += '.'

    return property(
        _getter if getter else None,
        _setter if setter else None,
        doc=doc
    )


# Programmatically set all internal field attributes for the Entry class
for field in bibpy.fields.all:
    doc = bibpy.fields.docstrings[field]

    setattr(Entry, "_" + field, None)
    setattr(Entry, field, autoproperty(field, True, True, doc=doc))
