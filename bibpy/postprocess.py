"""Conversion functions for pre- and postprocessing of bib(la)tex fields."""

import bibpy.compat
import bibpy.date
import bibpy.error
import bibpy.grammar
import bibpy.lexers
import bibpy.name
import bibpy.parser
import calendar
import re

_MONTH_ABBREVIATIONS = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun',
    'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
]

# TODO: Let users split on default names and custom ones
_SPLIT_NAMES = frozenset([
    'author', 'afterword', 'bookauthor', 'commentator',
    'editor', 'editora', 'editorb', 'editorc', 'foreword',
    'holder', 'introduction', 'language', 'origpublisher',
    'publisher', 'shortauthor', 'shorteditor', 'translator'
])


def postprocess_braces(value, **options):
    """Remove any braces from a string value."""
    if bibpy.compat.is_string(value):
        return "".join([e for e in bibpy.parser.parse_braced_expr(value)
                        if e not in '{}'])

    return value


def postprocess_namelist(field, names, **options):
    """Convert a string of authors to a list."""
    if not names:
        return []

    # First, split on zero brace-level 'and'
    names = bibpy.lexers.lex_namelist(names)

    # Second, if requested, parse each name
    if field in options.get('split_names', []):
        return [postprocess_name(field, n) for n in names]

    # Remove any leftover curly braces after splitting
    if not options.get('split_names', False):
        names = [re.sub('\{(.+?)\}', '\\1', name) for name in names]

    return names


def postprocess_name(field, author, **options):
    """Attempts to split an author name into first, middle and last name."""
    if author and bibpy.compat.is_string(author):
        return bibpy.name.Name.fromstring(author)
    else:
        return author


def postprocess_keywords(field, keywords, **options):
    """Convert a string of keywords to a list."""
    if not keywords:
        return []

    return [keyword.strip() for keyword in keywords.split(';')
            if keyword.strip()]


def postprocess_int(field, value, **options):
    """Convert a string to an integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


def postprocess_date(field, datestring, **options):
    """Convert a string to a bibpy.date.DateRange."""
    if not datestring:
        return bibpy.date.DateRange((None, None, None), (None, None, None),
                                    False)

    return bibpy.date.DateRange.fromstring(datestring)


def get_month_name(i):
    """Return the name of a month from its one-based index ."""
    return calendar.month_name[i]


def postprocess_month(field, month, **options):
    """Convert a month number to its name."""
    try:
        i = int(month)

        if i not in range(1, 13):
            return month

        return get_month_name(i)
    except (ValueError, IndexError):
        month_name = month.lower()

        if month_name in _MONTH_ABBREVIATIONS:
            # The first element of calendar.month_name is an empty string
            return get_month_name(_MONTH_ABBREVIATIONS.index(month_name) + 1)

    return month


def postprocess_keylist(field, keylist, **options):
    """Convert a comma-separated string of keys to a list."""
    if not keylist:
        return []

    return list(filter(None, [key.strip() for key in keylist.split(',')]))


def postprocess_pages(field, pages, **options):
    """Convert a page range to a 2-element tuple."""
    values = re.split('\-+', pages)

    if len(values) == 2:
        try:
            return (int(values[0]), int(values[1]))
        except (ValueError, TypeError):
            return pages
    else:
        return pages


# A dictionary of fields as keys and the functions that postprocess them as
# values, e.g. 'year' should be converted to an integer etc.
postprocess_functions = {'address':       postprocess_namelist,
                         'afterword':     postprocess_namelist,
                         'annotator':     postprocess_namelist,
                         'author':        postprocess_namelist,
                         'bookauthor':    postprocess_namelist,
                         'commentator':   postprocess_namelist,
                         'date':          postprocess_date,
                         'edition':       postprocess_int,
                         'editor':        postprocess_namelist,
                         'editora':       postprocess_namelist,
                         'editorb':       postprocess_namelist,
                         'editorc':       postprocess_namelist,
                         'eventdate':     postprocess_date,
                         'foreword':      postprocess_namelist,
                         'holder':        postprocess_namelist,
                         'institution':   postprocess_namelist,
                         'introduction':  postprocess_namelist,
                         'keywords':      postprocess_keywords,
                         'language':      postprocess_namelist,
                         'location':      postprocess_namelist,
                         'month':         postprocess_month,
                         'number':        postprocess_int,
                         'organization':  postprocess_namelist,
                         'origdate':      postprocess_date,
                         'origlocation':  postprocess_namelist,
                         'origpublisher': postprocess_namelist,
                         'pages':         postprocess_pages,
                         'pagetotal':     postprocess_int,
                         'publisher':     postprocess_namelist,
                         'related':       postprocess_keylist,
                         'school':        postprocess_namelist,
                         'shortauthor':   postprocess_namelist,
                         'shorteditor':   postprocess_namelist,
                         'translator':    postprocess_namelist,
                         'urldate':       postprocess_date,
                         'xdata':         postprocess_keylist,
                         'volume':        postprocess_int,
                         'year':          postprocess_int}


def postprocess(entry, fields, **options):
    """Postprocess a subset of fields in a list of parsed entries."""
    if type(fields) not in (bool, list):
        raise ValueError("postprocess takes either a bool or a list for fields"
                         ", not '{0}'".format(type(fields)))

    split_names = options.get('split_names', [])

    if type(split_names) not in (bool, list):
        raise ValueError("split_names takes either a bool or a list for fields"
                         ", not '{0}'".format(type(split_names)))

    remove_braces = options.get('remove_braces', False)
    _fields = []

    if fields:
        if type(fields) is bool:
            _fields = entry.fields
        elif type(fields) is list:
            _fields = fields
    elif remove_braces:
        _fields = entry.fields

    if type(split_names) is bool:
        split_names = _SPLIT_NAMES if split_names else []

    options['split_names'] = split_names

    for field in _fields:
        value = getattr(entry, field)

        if remove_braces:
            value = postprocess_braces(value, **options)

        if field in postprocess_functions:
            yield field, postprocess_functions[field](field, value, **options)
        else:
            yield field, value


# TODO: split_names should also work like postprocess and take the fields to
# postprocess as allowed
def postprocess_entry(entry, **options):
    """Convenience function for postprocessing the fields in an entry."""
    processed_fields =\
        bibpy.postprocess.postprocess(entry, options.get('postprocess', []),
                                      **options)

    for field, value in processed_fields:
        setattr(entry, field, value)
