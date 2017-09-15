"""Parsing functions."""

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
