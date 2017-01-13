"""Bib(la)tex grammars."""

import bibpy.entries
import bibpy.error
import bibpy.fields
import pyparsing as pp

# TODO: Speed up parsing! Parse graphs in 0.98s instead of 2.4Xs

##################################################################
# Shared grammar definitions
##################################################################
# 'key' in '@article{key, ...}'
KEY = pp.SkipTo(',')('entry key')

# Suppressed literals
ENTRY_START = pp.Suppress('@')
OPEN_BRACE = pp.Suppress('{')
CLOSED_BRACE = pp.Suppress('}')
OPEN_PARENTHESIS = pp.Suppress('(')
CLOSED_PARENTHESIS = pp.Suppress(')')
EQUAL_SIGN = pp.Suppress('=')
COMMA = pp.Suppress(',')

# A nested, balanced expression in braces, i.e. contents of fields, e.g.
# 'McAwesome' in 'author = {McAwesome}'
BRACED_EXPR = pp.Forward()
BRACED_EXPR <<= pp.originalTextFor('{' + pp.ZeroOrMore(BRACED_EXPR |
                                   pp.CharsNotIn('{}')) + '}')('braced value')
# NOTE: Do not rely on pyparsing.removeQuotes in the future
BRACED_EXPR.addParseAction(pp.removeQuotes)

PARENTHESISED_EXPR = (OPEN_PARENTHESIS + pp.CharsNotIn('()') +
                      CLOSED_PARENTHESIS)('parenthesised expression')

INTEGER = pp.Word(pp.nums)('integer')
VARIABLE = pp.Regex('[a-zA-Z]\w*')('variable')

QUOTED_VALUE = pp.QuotedString('"', escChar='\\',
                               multiline=True)('quoted value')

# For general string expressions that are parsed by the main parsing functions.
# A string expression is either a single double-quoted string or a combination
# of strings and variables
STRING_EXPR =\
    (QUOTED_VALUE |
     pp.originalTextFor(pp.delimitedList(QUOTED_VALUE | VARIABLE,
                                         delim='#')))('string expression')

# Used for string expansion
STRING_EXPR_EXPANSION =\
     (pp.delimitedList(QUOTED_VALUE |
                       VARIABLE, delim='#'))('string expression')


def base_grammar(valid_fields, valid_entries):
    """Generate base grammar which all other grammars are based on.

    The valid_fields and valid_entries arguments denote the allowable names for
    this grammar.

    """
    # Field values
    value = (BRACED_EXPR | INTEGER | VARIABLE | STRING_EXPR)('value')

    # Fields
    field = pp.Group(valid_fields + EQUAL_SIGN + value)('field')
    fields = ((pp.Group(pp.delimitedList(field, delim=',')) +
              pp.Optional(COMMA)) | pp.Group(pp.Empty()))('fields')

    # Entries
    entry_content = KEY + COMMA + fields
    braced_entry = (OPEN_BRACE + entry_content + CLOSED_BRACE)('braced entry')
    parenthesised_entry = (OPEN_PARENTHESIS + entry_content +
                           CLOSED_PARENTHESIS)('parenthesised entry')
    entry = pp.Group(ENTRY_START + valid_entries +
                     (braced_entry | parenthesised_entry))('entries')\
        .setResultsName('entries', listAllMatches=True)

    # '@string' entry
    braced_var = (OPEN_BRACE + VARIABLE + EQUAL_SIGN + value +
                  CLOSED_BRACE)('braced variable')
    parenthesised_var = (OPEN_PARENTHESIS + VARIABLE + EQUAL_SIGN +
                         value + CLOSED_PARENTHESIS)('parenthesised variable')

    string_entry = pp.Group(pp.CaselessKeyword('@string') +
                            (braced_var | parenthesised_var))('string entry')\
        .setResultsName('strings', listAllMatches=True)

    # '@comment' entry
    comment_entry = pp.Group(pp.CaselessKeyword('@comment') +
                             BRACED_EXPR)('comment entry')\
        .setResultsName('explicit_comments', listAllMatches=True)

    # @preamble entry
    preamble_entry =\
        pp.Group(pp.CaselessKeyword('@preamble') +
                 (BRACED_EXPR | PARENTHESISED_EXPR))('preamble entry')\
        .setResultsName('preambles', listAllMatches=True)

    # Comments (any not inside an entry)
    comments = (pp.CharsNotIn('@'))('comment')\
        .setResultsName('comments', listAllMatches=True)

    return pp.ZeroOrMore(string_entry |
                         comment_entry |
                         preamble_entry |
                         comments |
                         entry)


def bibtex_grammar():
    """Return a grammar for bibtex."""
    valid_fields = pp.oneOf(bibpy.fields.bibtex,  caseless=True)
    valid_entries = pp.oneOf(bibpy.entries.bibtex, caseless=True)

    return base_grammar(valid_fields, valid_entries)


# TODO: Test if biblatex (biber) can read @preamble etc. (it can read @string)
def biblatex_grammar():
    """Return a grammar for biblatex."""
    value = (BRACED_EXPR)('value')

    # Fields
    valid_fields = pp.oneOf(bibpy.fields.biblatex, caseless=True)
    field = pp.Group(valid_fields + EQUAL_SIGN + value)('field')
    fields = pp.Group(pp.delimitedList(field, delim=','))('fields')

    # Entries
    valid_entries = pp.oneOf(bibpy.entries.biblatex, caseless=True)
    entry = pp.Group(ENTRY_START + valid_entries +
                     OPEN_BRACE + KEY + COMMA +
                     fields + CLOSED_BRACE)('entries')\
        .setResultsName('entries', listAllMatches=True)

    # Comments (any not inside an entry)
    comments = (pp.CharsNotIn('@'))('comment')\
        .setResultsName('comments', listAllMatches=True)

    return pp.ZeroOrMore(entry | comments)


def mixed_grammar():
    """Generate a grammar for a mixed parser."""
    valid_fields = pp.oneOf(bibpy.fields.all, caseless=True)
    valid_entries = pp.oneOf(bibpy.entries.all, caseless=True)

    return base_grammar(valid_fields, valid_entries)


def relaxed_grammar():
    """Generate a grammar for a relaxed parser."""
    # The bibtex grammar is the most specific, so the relaxed grammar is based
    # on it. Therefore the relaxed grammar also covers the biblatex grammar.
    valid_field = pp.Regex('[a-zA-Z0-9_\-:\.]+')\
        .setParseAction(pp.downcaseTokens)
    valid_entry = pp.Regex('[a-zA-Z0-9_\-:\.]+')\
        .setParseAction(pp.downcaseTokens)

    return base_grammar(valid_field, valid_entry)


def date_grammar():
    """Generate a grammar for biblatex dates."""
    dash = pp.Suppress('-')
    forward_slash = pp.Suppress('/')
    year = pp.Regex('\d{4}')
    month = pp.Regex('\d{2}')
    day = pp.Regex('\d{2}')

    date = pp.Group(year + pp.Optional(dash + month) + pp.Optional(dash + day))
    grammar = date - pp.Optional(forward_slash ^ (forward_slash + date))

    return grammar

##################################################################
# Top-level Grammars
##################################################################
# Convenience dictionary for selecting reference formats
_formats = {
    'bibtex':   bibtex_grammar(),
    'biblatex': biblatex_grammar(),
    'mixed':    mixed_grammar(),
    'relaxed':  relaxed_grammar(),
    'date':     date_grammar()
}


def grammar_from_format(format):
    """Return the grammar correspoding to the given format string."""
    if format not in _formats:
        raise KeyError("Reference format '" + format + "' does not exist "
                       "(use any of " + ", ".join(sorted(_formats.keys())) +
                       ")")

    return _formats[format]
