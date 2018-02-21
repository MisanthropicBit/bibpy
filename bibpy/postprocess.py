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
        return [postprocess_name(field, name) for name in names]
    else:
        if options.get('remove_braces', False):
            # Remove any leftover curly braces
            return [re.sub('\{(.+?)\}', '\\1', name) for name in names]

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


def find_postprocess_fields(parameter, value):
    """Find the fields that need to be postprocessed for a given parameter."""
    if type(parameter) is bool:
        return value if parameter else []
    else:
        return parameter


def postprocess(entry, fields, **options):
    """Postprocess a subset of fields in a list of parsed entries."""
    remove_braces = find_postprocess_fields(options.get('remove_braces',
                                            False), entry.fields)
    split_names = find_postprocess_fields(options.get('split_names', False),
                                          _SPLIT_NAMES)
    fields = find_postprocess_fields(fields, entry.fields)

    postprocess_fields = set()
    postprocess_fields.update(remove_braces, split_names, fields)

    for field in postprocess_fields:
        value = getattr(entry, field, None)

        if value is not None and value != '':
            if field in fields and field in postprocess_functions:
                value = postprocess_functions[field](
                    field, value,
                    remove_braces=remove_braces,
                    split_names=split_names
                )

            if remove_braces:
                if type(value) is list:
                    value = [postprocess_braces(e, remove_braces=remove_braces,
                                                split_names=split_names)
                             for e in value]
                else:
                    value = postprocess_braces(value,
                                               remove_braces=remove_braces,
                                               split_names=split_names)

            setattr(entry, field, value)
