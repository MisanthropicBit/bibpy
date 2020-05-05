# -*- coding: utf-8 -*-

"""Base class for all types of entries."""


class BaseEntry:
    """Base class for all types of entries."""

    def format(self, **options):
        raise NotImplementedError()

    @property
    def bibtype(self):
        raise NotImplementedError()

    @property
    def bibkey(self):
        raise NotImplementedError()

    @property
    def fields(self):
        raise NotImplementedError()

    def aliases(self, format):
        raise NotImplementedError()

    def valid(self, format):
        raise NotImplementedError()

    def keys(self):
        raise NotImplementedError()

    def values(self):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        return not self == other

    def __contains__(self, item):
        raise NotImplementedError()

    def __getitem__(self, field):
        """Return the value for the given field."""
        raise NotImplementedError()

    def __iter__(self):
        for field in self.fields:
            yield (field, self[field])

    def __len__(self):
        raise NotImplementedError()

    def __str__(self):
        return self.format()

    def __repr__(self):
        raise NotImplementedError()
