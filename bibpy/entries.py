# -*- coding: utf-8 -*-

"""All valid bib(la)tex entry types.

As of the Biblatex package documentation version 3.2 (27/12/2015)

"""

__all__ = ('aliases', 'Entries')


base_entry_types = frozenset([
    'article',
    'book',
    'booklet',
    'inbook',
    'incollection',
    'inproceedings',
    'manual',
    'misc',
    'proceedings',
    'unpublished'
])

##################################################################
# Bibtex
##################################################################
bibtex_entry_types = frozenset([
    'conference',
    'masterthesis',
    'phdthesis',
    'techreport'
])

##################################################################
# Biblatex
##################################################################
# The set of all valid Biblatex entry types
biblatex_entry_types = frozenset([
    'bookinbook',
    'booklet',
    'collection',
    'inference',
    'mvbook',
    'mvcollection',
    'mvproceedings',
    'mvreference',
    'online',
    'patent',
    'periodical',
    'reference',
    'report',
    'set',
    'suppbook',
    'suppcollection',
    'suppperiodical',
    'thesis',
    'xdata'
])

# Unsupported entry types
biblatex_unsupported_entry_types = frozenset([
    'artwork',
    'audio',
    'bibnote',
    'commentary',
    'image',
    'juristiction',
    'legislation',
    'legal',
    'letter',
    'movie',
    'music',
    'performance',
    'review',
    'software',
    'standard',
    'video'
])

# Type aliases for all Biblatex entry types
biblatex_entry_type_aliases = {
    'inproceedings': ['conference'],
    'online':        ['electronic', 'www'],
    'report':        ['techreport'],
    'thesis':        ['masterthesis', 'phdthesis']
}

bibtex = base_entry_types | bibtex_entry_types
biblatex = base_entry_types\
    | biblatex_entry_types\
    | biblatex_unsupported_entry_types\
    | frozenset(
        [alias for value in biblatex_entry_type_aliases.values()
         for alias in value]
    )

all = biblatex | bibtex


def aliases(bibtype, format):
    """Return the biblatex aliases of the given entry type and format."""
    # There are no aliases in bibtex
    if format != 'biblatex':
        return []

    return biblatex_entry_type_aliases.get(bibtype, [])


class Entries:
    """Light-weight container object for parsed entries."""

    def __init__(self, entries=[], strings=[], preambles=[],
                 comment_entries=[], comments=[]):
        """Initialise with lists of bibliographic entries and comments."""
        self._entries = entries
        self._strings = strings
        self._preambles = preambles
        self._comment_entries = comment_entries
        self._comments = comments

    @property
    def entries(self):
        """A list of all bibliographic entries."""
        return self._entries

    @property
    def strings(self):
        """A list of all string entries."""
        return self._strings

    @property
    def preambles(self):
        """A list of all preamble entries."""
        return self._preambles

    @property
    def comment_entries(self):
        """A list of all comment entries."""
        return self._comment_entries

    @property
    def comments(self):
        """A list of all non-entry comments."""
        return self._comments

    @property
    def all_entries(self):
        """Return all entries (excluding comments) as a list."""
        return [
            self.strings,
            self.preambles,
            self.comment_entries,
            self.entries,
        ]

    @property
    def all(self):
        """Return all entries including comments."""
        return self.all_entries + [self.comments]

    def __iter__(self):
        """Iterate over all entries, including non-entry comments."""
        for entries in self.all:
            yield from entries

    def __getitem__(self, idx):
        return (
            self.strings,
            self.preambles,
            self.comment_entries,
            self.entries,
            self.comments,
        )[idx]

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return (
            '{0}(strings={1}, preambles={2}, comment_entries={3}, '
            'entries={4})'
        ).format(
            self.__class__.__name__,
            len(self.strings),
            len(self.preambles),
            len(self.comment_entries),
            len(self.entries)
        )
