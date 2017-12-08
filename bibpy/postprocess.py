"""Conversion functions for pre- and postprocessing of bib(la)tex fields."""

import bibpy.date
import bibpy.error
import bibpy.grammar
import bibpy.name
import bibpy.parser
import calendar
import re

# TODO: Sort order for names

_MONTH_ABBREVIATIONS = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun',
    'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
]


def postprocess_braces(value, **options):
    """Remove any braces from a string value."""
    # if not bibpy.is_string(value):
    #     return value
    return "".join([e for e in bibpy.parser.parse_braced_expr(value)
                    if e not in '{}'])


def postprocess_namelist(names, **options):
    """Convert a string of authors to a list."""
    if not names:
        return []

    split_on = re.compile('(?<!{)' + options.get('name_delimiter', 'and') +
                          '(?!})')

    # Split names on the chosen delimiter which is NOT surrounded by curly
    # braces
    names = list(filter(None, [n.strip() for n in split_on.split(names)]))

    # Remove any leftover curly braces after splitting
    names = [re.sub('\{(.+)\}', '\\1', name) for name in names]

    if options.get('split_names', False):
        return [postprocess_name(n) for n in names]

    return names


def postprocess_name(author, **options):
    """Attempts to split an author name into first, middle and last name."""
    if author and bibpy.compat.is_string(author):
        return bibpy.name.Name.fromstring(author)
    else:
        return author


def postprocess_keywords(keywords, **options):
    """Convert a string of keywords to a list."""
    if not keywords:
        return []

    delimiter = options.get('keyword_delimiter')

    if delimiter:
        return list(filter(None, [keyword.strip()
                                  for keyword in keywords.split(delimiter)]))


def postprocess_int(value, **options):
    """Convert a string to an integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


def postprocess_date(datestring, **options):
    """Convert a string to a bibpy.date.DateRange."""
    if not datestring:
        return bibpy.date.DateRange((None, None, None), (None, None, None),
                                    False)

    return bibpy.date.DateRange.fromstring(datestring)


def get_month_name(i):
    """Return the name of a month from its one-based index ."""
    return calendar.month_name[i]


def postprocess_month(month, **options):
    """Convert a month number to its name."""
    try:
        i = int(month)

        if i not in range(1, 13):
            raise bibpy.error.FieldError("month must be in range [1-12]")

        return get_month_name(i)
    except (ValueError, IndexError):
        month_name = month.lower()

        if month_name in _MONTH_ABBREVIATIONS:
            # The first element of calendar.month_name is an empty string
            return get_month_name(_MONTH_ABBREVIATIONS.index(month_name) + 1)

    return month


def postprocess_keylist(keylist, **options):
    """Convert a comma-separated string of keys to a list."""
    if not keylist:
        return []

    return list(filter(None, [key.strip() for key in keylist.split(',')]))


def postprocess_pages(pages, **options):
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
                         'author':        postprocess_namelist,
                         'bookauthor':    postprocess_namelist,
                         'commentator':   postprocess_namelist,
                         'date':          postprocess_date,
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
                         'organization':  postprocess_namelist,
                         'origdate':      postprocess_date,
                         'origlocation':  postprocess_namelist,
                         'origpublisher': postprocess_namelist,
                         'pages':         postprocess_pages,
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

    remove_braces = options.get('remove_braces', False)
    _fields = []

    if fields:
        if type(fields) is bool:
            _fields = entry.fields
        elif type(fields) is list:
            _fields = fields
    elif remove_braces:
        _fields = entry.fields

    for field in _fields:
        value = getattr(entry, field)

        if remove_braces:
            value = postprocess_braces(value, **options)

        if field in postprocess_functions:
            yield field, postprocess_functions[field](value, **options)
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
