"""Parsing functions using the pyparsing library."""

import bibpy.entry
import bibpy.grammar
import pyparsing as pp


# NOTE: Implement when pyparsing allows us to scan strings
def scan_string(string, format):  # pragma: no cover
    """Generate entries from a string for a given reference format."""
    grammar = bibpy.grammar.grammar_from_format(format)

    try:
        for entry in _extract_entries_scan(grammar.scanString(string), format):
            yield entry
    except pp.ParseBaseException as e:
        raise bibpy.error.ParseException(e.markInputline())


def scan_file(source, format):  # pragma: no cover
    """Scan the source and yield parsed tokens."""
    grammar = bibpy.grammar.grammar_from_format(format)

    try:
        return _extract_entries_scan(grammar.scanFile())
    except pp.ParseBaseException as e:
        raise bibpy.error.ParseException(e.markInputline())


def _extract_entries_scan(parsed_results, format):  # pragma: no cover
    """Internal function for extracting and yielding parsed results."""
    for tokens, _, _ in parsed_results:
        entry_type = tokens[0][0]

        if len(tokens[0]) == 3:
            if entry_type == 'string':
                yield bibpy.entry.String(tokens[1])
            elif entry_type == 'comment':
                yield bibpy.entry.Comment(tokens[1])
            elif entry_type == 'preamble':
                yield bibpy.entry.Preamble(tokens[1])
            else:
                yield bibpy.entry.Entry(entry_type, tokens[0][1],
                                        **tokens[0][2])
        else:
            yield tokens[0][0]


def parse(string, format):
    """Parse string using a given reference format."""
    grammar = bibpy.grammar.grammar_from_format(format)

    try:
        return _extract_entries(grammar.parseString(string, parseAll=True),
                                format)
    except pp.ParseBaseException as e:
        raise bibpy.error.ParseException(e.markInputline())


def parse_file(fh, format):
    """Parse a file using a given reference format."""
    grammar = bibpy.grammar.grammar_from_format(format)

    try:
        return _extract_entries(grammar.parseFile(fh, parseAll=True), format)
    except pp.ParseBaseException as e:
        raise bibpy.error.ParseException("{0}: '{1}'"
                                         .format(e, e.markInputline()))


def _extract_entries(parsed_results, format):
    """Internal function for extracting parsed results."""
    strings = [bibpy.entry.String(*s[1:])
               for s in parsed_results.get('strings', [])]

    preambles = [bibpy.entry.Preamble(*p[1:])
                 for p in parsed_results.get('preambles', [])]

    comment_entries = [bibpy.entry.Comment(c[1].strip())
                       for c in parsed_results.get('explicit_comments', [])]

    comments = list(filter(None,
                           [e.strip()
                            for e in parsed_results.get('comments', [])]))

    # We need to account for missing fields
    entries = [bibpy.entry.Entry(entry_type,
                                 entry_key,
                                 **dict(fields.asList()))
               for entry_type, entry_key, fields
               in parsed_results.get('entries', [])]

    return bibpy.entries.Entries(entries, strings, preambles, comment_entries,
                                 comments)


def parse_date(datestring):
    """Parse a biblatex date."""
    grammar = bibpy.grammar.grammar_from_format('date')

    try:
        return grammar.parseString(datestring, parseAll=True).asList()
    except pp.ParseException as e:
        raise bibpy.error.ParseException(e.markInputline())


def parse_string_expr(expr):
    """Parse a bibtex string expression."""
    if not expr:
        return expr

    try:
        return bibpy.grammar.STRING_EXPR_EXPANSION.parseString(expr,
                                                               parseAll=True)\
            .asList()
    except pp.ParseException:
        return expr


def parse_braced_string_expr(expr):
    """Parse a braced string and return its tokens."""
    return bibpy.grammar.BE.parseString(expr, parseAll=True).asList()


def key_grammar():
    """Return the grammar for parsing key queries."""
    return (pp.Combine(pp.Optional(pp.Literal('^') &
                       pp.Optional(pp.Literal('~'))) +
            pp.Regex('.+')))('key')


def entry_grammar():
    """Return the grammar for parsing name queries."""
    return (pp.Combine(pp.Optional(pp.Literal('^') &
                       pp.Optional(pp.Literal('~'))) +
            pp.Word(pp.alphas)))('entry')


def field_grammar():
    """Return the grammar for parsing field queries."""
    field_value = (pp.Optional(pp.Literal('^')) + pp.Word(pp.alphas) +
                   (pp.Literal('=') | pp.Literal('~')) +
                   pp.Regex('.+'))('field')

    field_occurrence = (pp.delimitedList(
        pp.Group(pp.Optional(pp.Literal('^')) + pp.Word(pp.alphas)),
        delim=','))('field_occurrence')

    return field_value | field_occurrence


def numeric_grammar():
    """Return the grammar for parsing year queries.

    Example queries are: '1900-1995' or '>= 1998'

    """
    integer = pp.Word(pp.nums)
    field_name = pp.Word(pp.alphas)  # pp.Regex('\w+')
    lt = pp.Literal('<')
    le = pp.Literal('<=')
    gt = pp.Literal('>')
    ge = pp.Literal('>=')

    # Simple comparisons
    # NOTE: We put le before lt to parse both
    comparison = (pp.Optional('^') + field_name + (le | lt | ge | gt) +
                  integer)('comparison')

    # Values can be given as intervals ('1990-2000')
    interval = (pp.Optional('^') + field_name + pp.Literal('=') + integer +
                pp.Suppress('-') + integer)('interval')

    # Values can be given as ranges ('1990<=year<=2000')
    # NOTE: We put le before lt to parse both
    range_ = (pp.Optional('^') + integer + (le | lt) + field_name + (le | lt) +
              integer)('range')

    return interval | comparison | range_


_GRAMMARS = {
    'entry_key':  key_grammar(),
    'entry_type': entry_grammar(),
    'field':      numeric_grammar() | field_grammar()
}


def parse_query(query, query_type):
    """Parse a query and return the operator and value.

    E.g. '~Author' is parsed as ('~', 'Author')

    """
    try:
        result = _GRAMMARS[query_type].parseString(query, parseAll=True)
        print result

        return result.getName(), result.asList()
    except pp.ParseException as e:
        raise bibpy.error.ParseException("Error: One or more constraints "
                                         "failed to parse at column " +
                                         str(e.col))
