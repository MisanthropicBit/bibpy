# -*- coding: utf-8 -*-

"""biblatex reference mappings (for crossref, xref and xdata fields)."""

_BOOK_COMMON_MAPPING = [
    ('title',          'booktitle'),
    ('subtitle',       'booksubtitle'),
    ('titleaddon',     'booktitleaddon'),
    ('shorttitle',     ''),
    ('sorttitle',      ''),
    ('indextitle',     ''),
    ('indexsorttitle', '')
]

_PROCEEDINGS_COMMON_MAPPING = [
    ('title',          'maintitle'),
    ('subtitle',       'mainsubtitle'),
    ('titleaddon',     'maintitleaddon'),
    ('shorttitle',     ''),
    ('sorttitle',      ''),
    ('indextitle',     ''),
    ('indexsorttitle', '')
]

# The default mapping if a source and target is not covered by the specific
# mappings given below. The 'None' target means that the field is mapped to the
# same field as is given in the source.
_DEFAULT_MAPPING = [
    (field, field) for field in [
        'ids',
        'crossref',
        'xref',
        'entryset',
        'entrysubtype',
        'execute',
        'label',
        'options',
        'presort',
        'related',
        'relatedoptions',
        'relatedstring',
        'relatedtype',
        'shorthand',
        'shorthandintro',
        'sortkey'
    ]
]

# This is an inverse mapping, i.e. target -> source, of the one given in
# biblatex to enable faster searches. The innermost lists are field mappings
# from the source to the target
mappings = {
    'mvbook': {
        'inbook': [
            ('author',         'author'),
            ('author',         'bookauthor'),
            ('title',          'maintitle'),
            ('subtitle',       'mainsubtitle'),
            ('titleaddon',     'maintitleaddon'),
            ('shorttitle',     ''),
            ('sorttitle',      ''),
            ('indextitle',     ''),
            ('indexsorttitle', '')
        ]
    }, 'mvcollection': {
        'collection': [('title', 'maintitle')]
    }, 'inbook': {
        'book': _BOOK_COMMON_MAPPING,
        'mvbook': [
            ('author', 'author'),
            ('author', 'bookauthor')
        ] + _PROCEEDINGS_COMMON_MAPPING
    }, 'book': {
        'mvbook': _PROCEEDINGS_COMMON_MAPPING
    }, 'collection': {
        'mvcollection': [('title', 'maintitle')]
    }, 'suppcollection': {
        'reference': [
            ('subtitle',       'mainsubtitle'),
            ('titleaddon',     'maintitleaddon'),
            ('shorttitle',     ''),
            ('sorttitle',      ''),
            ('indextitle',     ''),
            ('indexsorttitle', '')
        ]
    }, 'inproceedings': {
        'proceedings': _BOOK_COMMON_MAPPING
    }, 'article': {
        'periodical': [
            ('title',          'journaltitle'),
            ('subtitle',       'journaltitle'),
            ('shorttitle',     None),
            ('sorttitle',      None),
            ('indextitle',     None),
            ('indexsorttitle', None)
        ]
    },
}

# Set up similar mappings
mappings['bookinbook'] = mappings['inbook']
mappings['suppbook'] = mappings['inbook']
mappings['suppperiodical'] = mappings['article']


def inherit_crossrefs(source, target, inherit=True, override=False,
                      exceptions={}):
    """Update an entry with the fields from a crossreferenced entry."""
    if (target.bibtype, source.bibtype) in exceptions:
        # Handle special inheritance rules for this pair of entry types
        options = exceptions[(target.bibtype, source.bibtype)]
        inherit = options.get('inherit', inherit)
        override = options.get('override', override)

    if not inherit:
        return

    mapping = mappings.get(target.bibtype, {}).get(source.bibtype, []) +\
        _DEFAULT_MAPPING

    for source_field, target_field in mapping:
        if ((target_field in target and override) or
                target_field not in target) and source_field in source:
            setattr(target, target_field, getattr(source, source_field, None))


def uninherit_crossrefs(source, target, inherit='all', override=False,
                        exceptions={}):
    """Strip a target of the fields from a crossreferenced entry (source)."""
    if (target.bibtype, source.bibtype) in exceptions:
        # Handle special inheritance rules for this pair of entry types
        options = exceptions[(target.bibtype, source.bibtype)]
        inherit = options.get('inherit', inherit)
        override = options.get('override', override)

    if not inherit:
        return

    mapping = mappings.get(target.bibtype, {}).get(source.bibtype, []) +\
        _DEFAULT_MAPPING

    for source_field, target_field in mapping:
        source_value = getattr(source, source_field, None)
        target_value = getattr(target, target_field, None)

        # If the target contains the target field, the source contains the
        # source field and their values are identical, then it must been
        # inherited
        if target_field in target and source_field in source and\
                source_value == target_value:
            setattr(target, target_field, None)


def inherit_xdata(source, target):
    """Inherit all fields from source (xdata entry)."""
    # Though not stated in the biblatex manual, we do not let xdata inheritance
    # overwrite existing fields
    for field, value in source:
        if field not in target:
            setattr(target, field, value)


def uninherit_xdata(source, target):
    """Uninherit all fields in target inherited from source (xdata entry)."""
    for field, value in source:
        # Do not uninherit xdata fields
        if field in target and field != 'xdata':
            setattr(target, field, None)
