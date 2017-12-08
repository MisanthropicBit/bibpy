"""Conversion functions for pre- and postprocessing of bib(la)tex fields."""

import calendar
import re

_MONTHNAME_TO_INT = {v: k for k, v in enumerate(calendar.month_name)}


def preprocess_namelist(namelist, **options):
    """Convert a list of names to a delimited string."""
    if type(namelist) is not list:
        return namelist

    # First make sure that delimiter's are braced properly
    namelist = [re.sub('(and)', '{\\1}', name) for name in namelist]

    # Then return the delimited list of names
    return (' ' + options.get('namelist_delimiter', 'and') + ' ')\
        .join(namelist)


def preprocess_keywords(keywords, **options):
    """Convert a list of keywords to a delimited string."""
    if type(keywords) is not list:
        return keywords

    return options.get('keyword_delimiter', ';').join(keywords)


def preprocess_date(date, **options):
    """Preprocess a datetime and return its string equivalent."""
    return str(date)


def preprocess_month(month_name, **options):
    """Convert the name of a month to its one-based index."""
    return _MONTHNAME_TO_INT.get(month_name.capitalize(), month_name)


def preprocess_int(i, **options):
    """Convert a string to an integer."""
    return str(i)


def preprocess_keylist(keylist, **options):
    """Convert a list of keys to a comma-separated string."""
    if isinstance(keylist, list):
        return ", ".join([str(key) for key in keylist])

    return keylist


def preprocess_pages(pages, **options):
    """Convert a 2-element page range tuple to a string."""
    if isinstance(pages, tuple) and len(pages) == 2:
        return "{0}--{1}".format(pages[0], pages[1])

    return str(pages)


# A dictionary of fields as keys and the functions that preprocess them as
# values, e.g. 'year' should be converted to an integer etc.
preprocess_functions = {'address':       preprocess_namelist,
                        'afterword':     preprocess_namelist,
                        'author':        preprocess_namelist,
                        'bookauthor':    preprocess_namelist,
                        'chapter':       preprocess_int,
                        'commentator':   preprocess_namelist,
                        'date':          preprocess_date,
                        'edition':       preprocess_int,
                        'editor':        preprocess_namelist,
                        'editora':       preprocess_namelist,
                        'editorb':       preprocess_namelist,
                        'editorc':       preprocess_namelist,
                        'eventdate':     preprocess_date,
                        'foreword':      preprocess_namelist,
                        'holder':        preprocess_namelist,
                        'institution':   preprocess_namelist,
                        'introduction':  preprocess_namelist,
                        'keywords':      preprocess_keywords,
                        'language':      preprocess_namelist,
                        'location':      preprocess_namelist,
                        'month':         preprocess_month,
                        'number':        preprocess_int,
                        'organization':  preprocess_namelist,
                        'origdate':      preprocess_date,
                        'origlocation':  preprocess_namelist,
                        'origpublisher': preprocess_namelist,
                        'pages':         preprocess_pages,
                        'part':          preprocess_int,
                        'publisher':     preprocess_namelist,
                        'related':       preprocess_keylist,
                        'school':        preprocess_namelist,
                        'series':        preprocess_int,
                        'shortauthor':   preprocess_namelist,
                        'shorteditor':   preprocess_namelist,
                        'translator':    preprocess_namelist,
                        'urldate':       preprocess_date,
                        'xdata':         preprocess_keylist,
                        'volume':        preprocess_int,
                        'year':          preprocess_int}


def preprocess(entry, fields, **options):
    """Preprocess a subset of fields in a list of entries to be written."""
    for field in fields:
        value = getattr(entry, field, '')

        if field in preprocess_functions:
            yield field, preprocess_functions[field](value, **options)
        else:
            yield field, value
