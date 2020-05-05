# -*- coding: utf-8 -*-

"""Check entry requirements according to a reference format."""

YEAR_OR_DATE = frozenset(['year', 'date'])
AUTHOR_OR_EDITOR = frozenset(['author', 'editor'])

# Requirements for each entry type. Values are 2-tuples of the required fields
# and a list of fields where only one needs to be present
bibtex_requirements = {
    'article': (
        frozenset(['author',
                   'title',
                   'journal',
                   'year']),
        []
    ), 'book': (
        frozenset(['title',
                   'publisher',
                   'year']),
        [AUTHOR_OR_EDITOR]
    ), 'booklet': (
        frozenset(['title']),
        []
    ), 'inbook': (
        frozenset(['title',
                   'publisher',
                   'year']),
        [AUTHOR_OR_EDITOR,
         frozenset(['chapter', 'pages'])]
    ), 'incollection': (
        frozenset(['author',
                   'title',
                   'booktitle',
                   'publisher',
                   'year']),
        []
    ), 'inproceedings': (
        frozenset(['author',
                   'title',
                   'booktitle',
                   'year']),
        []
    ), 'manual': (
        frozenset(['title']),
        []
    ), 'masterthesis': (
        frozenset(['author',
                   'title',
                   'school',
                   'year']),
        []
    ), 'misc': (
        frozenset(),
        []
    ), 'phdthesis': (
        frozenset(['author',
                   'title',
                   'school',
                   'year']),
        []
    ), 'proceedings': (
        frozenset(['title',
                   'year']),
        []
    ), 'techreport': (
        frozenset(['author',
                   'title',
                   'institution',
                   'year']),
        []
    ), 'unpublished': (
        frozenset(['author',
                   'title',
                   'note']),
        []
    )
}

bibtex_requirements['conference'] = bibtex_requirements['inproceedings']

biblatex_requirements = {
    'article': (
        frozenset(['author',
                   'title',
                   'journaltitle']),
        [YEAR_OR_DATE]
    ), 'book': (
        frozenset(['author',
                   'title']),
        [YEAR_OR_DATE]
    ), 'mvbook': (
        frozenset(['author',
                   'title']),
        [YEAR_OR_DATE]
    ), 'booklet': (
        frozenset(['title']),
        [AUTHOR_OR_EDITOR, YEAR_OR_DATE]
    ), 'mvcollection': (
        frozenset(['editor', 'title']),
        [YEAR_OR_DATE]
    ), 'collection': (
        frozenset(['editor', 'title']),
        [YEAR_OR_DATE]
    ), 'incollection': (
        frozenset(['author',
                   'title',
                   'booktitle']),
        [YEAR_OR_DATE]
    ), 'manual': (
        frozenset(['title']),
        [AUTHOR_OR_EDITOR, YEAR_OR_DATE]
    ), 'misc': (
        frozenset(),
        []
    ), 'online': (
        frozenset(['title', 'url']),
        [AUTHOR_OR_EDITOR, YEAR_OR_DATE]
    ), 'patent': (
        frozenset(['author', 'title', 'number']),
        [YEAR_OR_DATE]
    ), 'periodical': (
        frozenset(['editor', 'title']),
        [YEAR_OR_DATE]
    ), 'proceedings': (
        frozenset(['title']),
        [YEAR_OR_DATE]
    ), 'inproceedings': (
        frozenset(['author',
                   'title',
                   'booktitle']),
        [YEAR_OR_DATE]
    ), 'report': (
        frozenset(['author',
                   'title',
                   'type',
                   'institution']),
        [YEAR_OR_DATE]
    ), 'set': (
        # ???
    ), 'thesis': (
        frozenset(['author',
                   'title',
                   'type',
                   'institution']),
        [YEAR_OR_DATE]
    ), 'unpublished': (
        frozenset(['author', 'title']),
        [YEAR_OR_DATE]
    ), 'xdata': (
        frozenset(),
        []
    )}

mixed_requirements = {}  # Possible?

# Set aliases for requirements
biblatex_requirements['report'] = biblatex_requirements['collection']

# Convenience dictionary for selecting reference formats
formats = {
    'bibtex':   bibtex_requirements,
    'biblatex': biblatex_requirements,
    'mixed':    mixed_requirements
}


def check(entry, format):
    """Check that an entry abides by the format's requirements.

    Note that these requirements are not strictly enforced in bibtex or
    biblatex. They are more guidelines for achieving well-formatted entries in
    your bibliography.

    """
    if format in ('relaxed', 'mixed'):
        return (frozenset(), [])

    if format not in formats:
        raise ValueError("Unknown reference format '" + format + "'")

    requirements = formats[format]
    fields = frozenset(entry.fields)
    required, either = requirements.get(entry.bibtype, (frozenset(), []))

    # We return sets to enable easy comparison between requirements since
    # set([1, 2]) == set([2, 1]), but [1, 2] != [2, 1]
    return set(required - fields), [set(e) for e in either
                                    if fields.isdisjoint(e)]


def collect(entries, format):
    """Collect all missing requirements for a set of entries."""
    result = []

    for entry in entries:
        required, optional = check(entry, format)

        if required or optional:
            result.append((entry, (required, optional)))

    return result
