# -*- coding: utf-8 -*-

"""Class representing single entries in a bib(la)tex file."""

import bibpy.entries
import bibpy.error
import bibpy.fields
import bibpy.requirements
from bibpy.entry import base


# TODO: Fix writing string expressions
class Entry(base.BaseEntry):
    """Represents an entry in a bib(la)tex file."""

    def __init__(self, entry_type, entry_key, **fields):
        """Create a bib entry and set fields."""
        self._fields = set(fields.keys())
        self._entry_type = entry_type
        self._entry_key = entry_key

        for field, value in fields.items():
            if field in bibpy.fields.all:
                f = field.lower()
                setattr(self, "_" + f, value)
            else:
                setattr(self, field, value)

    # TODO: How can we test this across versions?
    def format(self, align=True, indent='    ', order=[], surround='{}',
               **kwargs):  # pragma: no cover
        """Format and return the entry as a string.

        'align' aligns the equal signs of all fields.
        'indent' controls the amount of indentation inside an entry.
        'order' is a list of the order of a subset of fields.

        """
        entry_start = "@" + self.entry_type + "{" + self.entry_key + ",\n"

        if not self.fields:
            return entry_start + "}"

        i = max(map(len, self.fields)) if align else 1
        fields = []

        if order:
            if type(order) is bool:
                fields = sorted(bibpy.preprocess.preprocess(self, self.fields))
            elif type(order) is list:
                order = [o for o in order if getattr(self, o, None)]
                fields = list(bibpy.preprocess.preprocess(self, order)) +\
                    list(bibpy.preprocess.preprocess(self,
                                                     [f for f in self.fields
                                                      if f not in order]))
            else:
                raise ValueError("order must be either a bool or a list, not "
                                 "'{0}'".format(type(order)))
        else:
            for field, value in bibpy.preprocess.preprocess(self, self.fields):
                setattr(self, field, value)
                fields.append((field, value))

        fields = (",\n".join(["{0}{1}{2} = {3}{4}{5}"
                              .format(indent, field,
                                      ' ' * (i - len(field)),
                                      surround[0], value, surround[1])
                             for field, value in fields]))

        return entry_start + fields + "\n}"

    @property
    def entry_type(self):
        """Return the entry type of this entry."""
        return self._entry_type

    @entry_type.setter
    def entry_type(self, value):
        self._entry_type = value

    @property
    def entry_key(self):
        """Return the key of this entry."""
        return self._entry_key

    @entry_key.setter
    def entry_key(self, value):
        self._entry_key = value

    @property
    def fields(self):
        """Return a list of this entry's active bib(la)tex fields.

        Active fields are fields that are not None or empty strings.

        """
        return [prop for prop in vars(self) if not prop.startswith('_')
                if getattr(self, prop)] +\
            [field for field in bibpy.fields.all if getattr(self, field)]

    @property
    def extra_fields(self):
        """Return any extra fields not recognised as bibtex or biblatex."""
        return [prop for prop in vars(self) if not prop.startswith('_')]

    def get(self, name, default=None):
        """Return the value for name or default if the name does not exist."""
        return getattr(self, name, default)

    def aliases(self, format):
        """Return any aliases of this entry."""
        return bibpy.entries.aliases(self.entry_type, format)

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
        """Entries are equal if their fields and values match."""
        if not isinstance(other, Entry):
            return False

        if self.entry_type != other.entry_type or\
                self.entry_key != other.entry_key:
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
        """Check if a field is set for this entry."""
        return item in self.fields

    def __getattr__(self, name):
        return None

    def __setattr__(self, name, value):
        super(Entry, self).__setattr__(name, value)

        if value == '' or value is None:
            if name in self._fields:
                self._fields.remove(name)
        else:
            self._fields.add(name)

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
        """Return the same string representation as __str()__."""
        return "Entry(type={0}, key={1})".format(self.entry_type,
                                                 self.entry_key)


def autoproperty(name, getter=True, setter=True, prefix='_'):
    """Autogenerate a property."""
    attribute = prefix + name

    def _getter(self):
        return getattr(self, attribute)

    def _setter(self, value):
        # Update the entry's list of active fields
        if value is None or value == '':
            if name in self._fields:
                self._fields.remove(name)
        else:
            self._fields.add(name)

        setattr(self, attribute, value)

    return property(_getter if getter else None,
                    _setter if setter else None)


# Programmatically set all internal field attributes for the Entry class
for field in bibpy.fields.all:
    setattr(Entry, "_" + field, None)
    setattr(Entry, field, autoproperty(field, True, True))
