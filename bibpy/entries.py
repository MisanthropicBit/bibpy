"""All valid bib(la)tex entry types.

As of the Biblatex package documentation version 3.2 (27/12/2015)

"""

import collections


base_entry_types = frozenset(
    ['article',
     'book',
     'booklet',
     'inbook',
     'incollection',
     'inproceedings',
     'manual',
     'misc',
     'proceedings',
     'unpublished']
)

##################################################################
# Bibtex
##################################################################
bibtex_entry_types = frozenset(
    ['conference',
     'masterthesis',
     'phdthesis',
     'techreport']
)

##################################################################
# Biblatex
##################################################################
# The set of all valid Biblatex entry types
biblatex_entry_types = frozenset(
    ['bookinbook',
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
     'xdata']
)

# Unsupported entry types
biblatex_unsupported_entry_types = frozenset(
    ['artwork',
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
     'video']
)

# Type aliases for all Biblatex entry types
biblatex_entry_type_aliases = {
    'inproceedings': ['conference'],
    'online':        ['electronic', 'www'],
    'report':        ['techreport'],
    'thesis':        ['masterthesis', 'phdthesis']
}

bibtex = base_entry_types | bibtex_entry_types
biblatex = base_entry_types | biblatex_entry_types |\
    biblatex_unsupported_entry_types |\
    frozenset([v for l in biblatex_entry_type_aliases.values() for v in l])

all = biblatex | bibtex


def aliases(entry_type, format):
    """Return the aliases of the given entry type and format."""
    # There are no aliases in bibtex
    if format != 'biblatex':
        return []

    return biblatex_entry_type_aliases.get(entry_type, [])


# Light-weight container object for parsed entries
Entries = collections.namedtuple('Entries', ['entries', 'strings', 'preambles',
                                             'comment_entries', 'comments'])
