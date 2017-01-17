# -*- coding: utf-8 -*-

"""bibpy: Bib(la)tex parser and tools."""

import bibpy.parse
import bibpy.postprocess
import bibpy.preprocess
import bibpy.references
import io
import os
import re
import sys

__version__ = '0.1.0'
__license__ = 'MIT'
__author__ = 'Alexander Asp Bock'
__all__ = ('read_string',
           'read_file',
           'write_string',
           'write_file',
           'is_format',
           'is_format_file',
           'expand_strings',
           'unexpand_strings',
           'inherit_crossrefs',
           'uninherit_crossrefs',
           'inherit_xdata',
           'uninherit_xdata')

__BIBPY_PY3__ = sys.version_info[0] > 2


def is_string(s):  # pragma: no cover
    """Check if the argument is a string or not."""
    if __BIBPY_PY3__:
        return isinstance(s, str)
    else:
        return isinstance(s, basestring)


def read_string(string, format, strict=False, postprocess=False,
                name_delimiter='and', keyword_delimiter=';'):
    """Read a string containing references in a given format.

    The function returns a 5-tuple of parsed entries and comments.

    Valid formats are 'bibtex', 'biblatex', 'mixed' or 'relaxed':
        bibtex  : Parse as bibtex, raise error on non-conformity
        biblatex: Parse as biblatex, raise error on non-conformity
        mixed   : Parse as a mix of bibtex and biblatex, raise error on non-
                  conformity
        relaxed : Allow any type of entries or fields

    'postprocess' can either be a list of fields to convert or a bool. If True,
    then all viable entry fields are converted to appropriate types, more
    specifically:

        Fields                                    Target type
        =======================================================================
        * year                                    int
        * month                                   Month name ('January' etc.)
        * date, eventdate, origdate, urldate      bibpy.date.DateRange
        * afterword, author, bookauthor,
          commentator, editor, editora, editorb,
          editorc, foreword, holder, institution,
          introduction, keywords, language,
          location, organization, origlocation,
          origpublisher, publisher, shortauthor,
          shorteditor, translator                 List of names
        * xdata                                   List of keys

    Use 'name_delimiter' as a delimiter for author lists etc. if 'postprocess'
    is enabled, such that 'Myers and Gregg' -> ['Myers', 'Gregg']

    Use 'keyword_delimiter' as a delimiter for keywords if 'postprocess'
    is enabled, such that 'keyword1; keyword2' -> ['keyword1', 'keyword2'].
    Note that keywords are stripped of surrounding whitespaces.

    """
    return _read_common(bibpy.parse.parse(string, format), format, strict,
                        postprocess, name_delimiter, keyword_delimiter)


def read_file(source, format, encoding='utf-8', strict=False,
              postprocess=False, name_delimiter='and', keyword_delimiter=';'):
    """Read a file containing references in a given format.

    The 'source' argument can either be a file handle or a filename. Files are
    treated as utf-8 encoded by default. The function returns a 5-tuple of
    parsed entries and comments.

    Valid formats are 'bibtex', 'biblatex', 'mixed' or 'relaxed':
        bibtex  : Parse as bibtex, raise error on non-conformity
        biblatex: Parse as biblatex, raise error on non-conformity
        mixed   : Parse as a mix of bibtex and biblatex, raise error on non-
                  conformity
        relaxed : Allow any type of entries or fields

    'postprocess' can either be a list of fields to convert or a bool. If True,
    then all viable entry fields are converted to appropriate types, more
    specifically:

        Fields                                    Target type
        =======================================================================
        * year                                    int
        * month                                   Month name ('January' etc.)
        * date, eventdate, origdate, urldate      bibpy.date.DateRange
        * afterword, author, bookauthor,
          commentator, editor, editora, editorb,
          editorc, foreword, holder, institution,
          introduction, keywords, language,
          location, organization, origlocation,
          origpublisher, publisher, shortauthor,
          shorteditor, translator                 List of names
        * xdata                                   List of keys

    Use 'name_delimiter' as a delimiter for author lists etc. if 'postprocess'
    is enabled, such that 'Myers and Gregg' -> ['Myers', 'Gregg']

    Use 'keyword_delimiter' as a delimiter for keywords if 'postprocess'
    is enabled, such that 'keyword1; keyword2' -> ['keyword1', 'keyword2'].
    Note that keywords are stripped of surrounding whitespaces.

    """
    fh = (io.open(source, encoding=encoding) if is_string(source) else source)

    with fh:
        return _read_common(bibpy.parse.parse_file(fh, format), format, strict,
                            postprocess, name_delimiter, keyword_delimiter)


def _read_common(parsed_tokens, format, strict=False, postprocess=False,
                 name_delimiter='and', keyword_delimiter=';'):
    """Internal function for processing parsed tokens."""
    entries = parsed_tokens

    if strict:
        # Check entry requirements for non-relaxed reference formats
        for entry in entries.entries:
            required, optional = bibpy.requirements.check(entry, format)

            if required or optional:
                raise bibpy.error.RequiredFieldError(entry, required, optional)

    # Postprocess a subset of fields for automatic type conversion
    if postprocess:
        for entry in entries.entries:
            for field, value in\
                bibpy.postprocess.postprocess(
                    entry,
                    postprocess,
                    name_delimiter=name_delimiter,
                    keyword_delimiter=keyword_delimiter):
                setattr(entry, field, value)

    return entries


def write_string(entries, **format_options):
    """Write a list of entries as a string.

    The list of formatting options are the same as those for entry.format.

    """
    return (os.linesep * 2).join(entry.format(**format_options)
                                 for entry in entries)


def write_file(source, entries, encoding='utf-8', **format_options):
    """Write a list of entries to a file given by a filename or file descriptor.

    The list of formatting options are the same as those for entry.format.

    """
    if is_string(source):
        source = io.open(source, 'w', encoding=encoding)

    with source as fh:
        fh.write(bibpy.write_string(entries, **format_options))


def is_format(string, format):
    """Check whether the string conforms to the given reference format."""
    try:
        read_string(string, format)
        return True
    except bibpy.error.ParseException:
        return False


def is_format_file(file, format):
    """Check whether the file conforms to the given reference format."""
    try:
        read_file(file, format)
        return True
    except bibpy.error.ParseException:
        return False


def _find_duplicate_variables(strings):
    """Find all string variables that appear more than once."""
    seen = set()
    duplicates = []

    for string in strings:
        var = string.variable

        if var in seen:
            duplicates.append(var)
        else:
            seen.add(var)

    return duplicates


def expand_strings(entries, strings, ignore_duplicates=False):
    """Expand all string variables found in all entries.

    The operation is done in-place. If multiple string variables have the same
    name, only one of them is arbitrarily used unless ignore_duplicates is True
    in which case an exception is thrown.

    """
    if not entries or not strings:
        return

    if not ignore_duplicates:
        duplicates = _find_duplicate_variables(strings)

        if duplicates:
            raise ValueError("Strings contain duplicate variables: " +
                             ", ".join(duplicates))
    # For faster lookup
    variables = dict((var, val) for string in strings for var, val in string)

    for entry in entries:
        for field, value in entry:
            if is_string(value):
                exprs = bibpy.parse.parse_string_expr(value)
                expanded = "".join([variables.get(expr, expr)
                                    for expr in exprs])
                setattr(entry, field, expanded)


def unexpand_strings(entries, strings, ignore_duplicates=False):
    """Unexpand all string variables in all entries where possible.

    The operation is done in-place. If multiple string variables have the same
    name, only one of them is arbitrarily used unless ignore_duplicates is True
    in which case an exception is thrown.

    """
    if not entries or not strings:
        return

    if not ignore_duplicates:
        duplicates = _find_duplicate_variables(strings)

        if duplicates:
            raise ValueError("Strings contain duplicate variables: " +
                             ", ".join(duplicates))

    # For faster lookup
    values = dict((val, var) for string in strings for var, val in string)
    value_regex = re.compile('(' + "|".join(map(re.escape, values.keys())) +
                             ')')

    for entry in entries:
        for field, value in entry:
            if is_string(value):
                temp = re.split(value_regex, value)

                if len(temp) > 1:
                    value =\
                        " # ".join(['"' + v + '"' if v not in values
                                    else values[v]
                                    for v in filter(None, temp)])

                setattr(entry, field, value)


def _crossref_common(entries, ref_func, inherit=True, override=False,
                     exceptions={}):
    """Common function for inheritance and uninheritance of crossreferences."""
    if not entries or not inherit:
        return

    # For faster lookup
    crossref_keys = {}
    targets = []

    for entry in entries:
        # Only examine the entries that contain a crossref field
        if entry.crossref:
            targets.append(entry)

        # All entries can be sources of a crossref field
        crossref_keys[entry.entry_key] = entry

    for entry in targets:
        if entry.crossref in crossref_keys:
            source = crossref_keys[entry.crossref]

            ref_func(source, entry, inherit, override, exceptions)


def inherit_crossrefs(entries, inherit=True, override=False, exceptions={}):
    """Expand the crossreferences in the given entries.

    The expansion is done according to biber (see section 2.4.1 of the biblatex
    manual).

    Inheritance modes are either True for inheriting or False for no
    inheritance. Likewise fields can either be overwritten or not. Note that
    overriding fields is a destructive process, they cannot be recreated by
    unexpand_crossrefs.

    Expections to both rules can be defined using the exceptions option which
    is expected to be a tuple of (source, target, options), where the source is
    the crossrefered entry and target is the entry containing the crossref, as
    per biblatex nomenclature. The last field is a dict of the options (inherit
    and override) for this pair of source and target.

    """
    _crossref_common(entries, bibpy.references.inherit_crossrefs, inherit,
                     override, exceptions)


def uninherit_crossrefs(entries, inherit=True, override=False, exceptions={}):
    """Unexpand or collapse the crossreferences in the given entries.

    The unexpansion is done according to biber (see section 2.4.1 of the
    biblatex manual). The 'crossref' fields of the entries are used if they
    refer to a valid key.

    The options correspond to those given by the a call to expand_crossrefs.

    Inheritance modes are either 'all' (True) or 'none' (False). Fields can
    either be overwritten or not. Expections to both rules can be defined using
    the 'exceptions' option which is expected to be a dictionary mapping from
    one entry type to another and the value the 'inherit' and/or 'override'
    options. Both the source and the target can be '*' to denote all entry
    types.

    """
    _crossref_common(entries, bibpy.references.uninherit_crossrefs, inherit,
                     override, exceptions)


def _filter_xdata_by_keys(entry, xdata_keys):
    """Filter and return the xdata keys in entry that are in xdata_keys."""
    return [xdata_keys[xdata_key] for xdata_key in
            bibpy.postprocess.postprocess_keylist(entry.xdata)
            if xdata_key in xdata_keys]


def _xdata_common(entries, xdata_func):
    """Common function for inheritance and uninheritance of xdata fields."""
    if not entries:
        return

    # For faster lookup
    xdata_keys = dict((entry.entry_key, entry) for entry in entries
                      if entry.entry_type == 'xdata')

    if not xdata_keys:
        return

    for entry in entries:
        sources = _filter_xdata_by_keys(entry, xdata_keys)

        # xdata entries can cascade
        while sources:
            source = sources.pop(0)

            xdata_func(source, entry)

            # xdata entries can cascade
            sources += _filter_xdata_by_keys(source, xdata_keys)


def inherit_xdata(entries):
    """Expand the xdata fields in the given entries.

    The expansion is done according to biber (see section 3.11.6 of the
    biblatex manual).

    """
    _xdata_common(entries, bibpy.references.inherit_xdata)


def uninherit_xdata(entries):
    """Unherit the xdata fields in the given entries.

    The uninheritance is done according to biber (see section 3.11.6 of the
    biblatex manual).

    """
    _xdata_common(entries, bibpy.references.uninherit_xdata)
