# -*- coding: utf-8 -*-

"""Parsing functions using the funcparserlib library."""

import bibpy.date
import bibpy.entry
import bibpy.lexers
from bibpy.name import Name
from bibpy.tools import always_true
import funcparserlib.parser as parser
import funcparserlib.lexer as lexer
import re


def token_value(token):
    """Get the value from a token."""
    return token.value


def token_type(token_type):
    """Match a given token type and return its value."""
    return parser.some(lambda x: x.type == token_type) >> token_value


def if_token_type(token_type, pred):
    """Return a parser that parses a token type for which a predicate holds."""
    return parser.some(lambda t: t.type == token_type and pred(t.value))


def skip(s):
    """Parse and skip a specific token type."""
    return parser.skip(parser.some(lambda x: x.type == s))


def simple_entry(content, matcher, producer):
    return skip('entry') + if_token_type('name', matcher) +\
        (enclosed('lbrace', 'rbrace', content) |
         enclosed('lparen', 'rparen', content)) >> producer


def make_string(token):
    """Make a string from a token."""
    return token.value.strip()


def flatten(lst):
    """Flatten a list of an arbitrary depth."""
    for e in lst:
        if isinstance(e, list):
            for i in e:
                yield i
        else:
            yield e


def make_braced_expr(tokens):
    """Make a braced expr from a recursive, nested list of tokens."""
    result = ""

    for e in tokens[1:-1]:
        if isinstance(e, list):
            result += "".join([getattr(t, 'value', t) for t in flatten(e)])
        else:
            result.append(e.value)

    contents = ''.join([getattr(token, 'content', token) for token in result])

    return tokens[0].value + contents + tokens[2].value


def make_list(tokens):
    """Make a list from the list of parsed tokens."""
    return [tokens[0]] + tokens[1]


def make_field(tokens):
    """Make a field from two tokens."""
    return tokens[0].value.strip().lower(), tokens[1]


def make_string_entry(tokens):
    """Make a bib string entry from a list of parsed tokens."""
    bibtype, [var, value] = tokens

    return bibpy.entry.String(var, value.strip('"'))


def make_comment_entry(tokens):
    """Make a comment entry from a list of parsed tokens."""
    bibtype, value = tokens

    return bibpy.entry.Comment(value)


def make_preamble_entry(tokens):
    """Make a preamble entry from a list of parsed tokens."""
    bibtype, value = tokens

    return bibpy.entry.Preamble(value)


def get_duplicates(iterable):
    """Find and return any duplicates in the iterable."""
    duplicates = {}

    for i in iterable:
        duplicates.setdefault(i, 0)
        duplicates[i] += 1

    return [d for d in duplicates if duplicates[d] > 1]


def make_entry(tokens):
    """Make a bib entry from a list of parsed tokens."""
    bibtype = tokens[0].lower()
    bibkey = tokens[1]
    fields = tokens[2] if tokens[2] is not None else []
    fields = [(f.lower(), v) for f, v in fields]

    duplicates = get_duplicates([f[0] for f in fields])

    if duplicates:
        msg = "Duplicate field(s) '{0}' in entry '{1}' with type '{2}'"\
            .format(', '.join(duplicates), bibkey, bibtype)
        raise bibpy.error.ParseException(msg)

    return bibpy.entry.Entry(bibtype, bibkey, fields=fields)


def make_date(tokens):
    """Make a DateRange from a list of tokens."""
    start = tuple(tokens[:3])
    end = (None, None, None)
    open_ended = False

    if tokens[3]:
        if tokens[3] == '/':
            open_ended = True
        elif tokens[3][0] == '/':
            end = tuple(tokens[3][1])

    return bibpy.date.DateRange(start, end, open_ended)


def is_string_entry(token):
    return token.lower() == 'string'


def is_comment_entry(token):
    return token.lower() == 'comment'


def is_preamble_entry(token):
    return token.lower() == 'preamble'


def remove_outer_braces(braced_expr):
    """Remove the outer braces from a braced expression."""
    return braced_expr[1:-1]


def enclosed(start, end, inner):
    """Parse an enclosed expression and skip delimiters."""
    return skip(start) + inner + skip(end)


def join_string_expr(delimiter):
    """Return a function that can join string expressions."""
    def _join_string_expr(tokens):
        if len(tokens) == 1:
            return tokens[0].strip('"')
        else:
            result = [tokens[0]]

            for token in tokens[1:]:
                result.extend(token)

            return ''.join(result)

    return _join_string_expr


def delimited_list(element, separator):
    """Create a parser of a list of delimited tokens."""
    return element + parser.many(parser.skip(token_type(separator)) + element)\
        >> make_list


def full_delimited_list(element, separator):
    """Create a parser of a list of delimited tokens, keeping delimiters."""
    return element + parser.many(token_type(separator) + element) >> make_list


def base_parser(validate_field, validate_entry):
    """Return the base parser which all other parsers are based on.

    The valid_fields and valid_entries arguments denote the allowable names for
    a grammar.

    """
    # Simple expressions
    integer = token_type('number')
    name = token_type('name')
    variable = name

    # Braced expressions e.g. '{braced}'
    non_braced = if_token_type('content', always_true)
    braced_expr = parser.forward_decl()
    braced_expr.define(
        (if_token_type('lbrace', lambda v: True) +
         parser.many(braced_expr | non_braced) +
         if_token_type('rbrace', lambda v: True)) >> make_braced_expr
    )
    braced_expr = braced_expr >> remove_outer_braces

    # String expressions, e.g. '"This " # var # " that"'
    string_expr =\
        full_delimited_list(
            parser.some(lambda x: x.type == 'string') >> make_string |
            parser.some(lambda x: x.type == 'name') >> token_value,
            'concat'
        ) >> join_string_expr('')

    # The value of a field
    value = braced_expr | integer | string_expr | variable

    # Make sure we only parsed valid fields
    valid_field = if_token_type('name', validate_field)

    field = valid_field + skip('equals') + value >> make_field

    assignment = token_type('name') + skip('equals') + value

    # A regular comment: Any text outside of entries
    comment = token_type('comment')

    # @string
    string_entry = simple_entry(
        assignment,
        is_string_entry,
        make_string_entry
    )

    # @comment
    comment_entry = simple_entry(
        token_type('content'),
        is_comment_entry,
        make_comment_entry
    )

    # @preamble
    preamble_entry = simple_entry(
        token_type('content'),
        is_preamble_entry,
        make_preamble_entry
    )

    # Make sure we only parsed valid entries
    valid_entry = if_token_type('name', validate_entry) >> token_value

    # @article etc.
    entry = skip('entry')\
        + valid_entry\
        + skip('lbrace')\
        + (token_type('name') | token_type('number')) + skip('comma')\
        + parser.maybe(delimited_list(field, 'comma'))\
        + parser.maybe(skip('comma'))\
        + skip('rbrace')\
        >> make_entry

    return parser.many(
        string_entry
        | comment_entry
        | preamble_entry
        | entry
        | comment
    ) + parser.skip(parser.finished)


def bibtex_parser():
    """Return a parser for bibtex."""
    def validate_field(field):
        return field.lower().strip() in bibpy.fields.bibtex

    def validate_entry(entry):
        return entry.lower().strip() in bibpy.entries.bibtex

    return base_parser(validate_field, validate_entry)


def biblatex_parser():
    """Return a parser for biblatex."""
    def validate_field(field):
        return field.lower().strip() in bibpy.fields.biblatex

    def validate_entry(entry):
        return entry.lower().strip() in bibpy.entries.biblatex

    return base_parser(validate_field, validate_entry)


def mixed_parser():
    """Return a mixed (bibtex/biblatex) parser."""
    def validate_field(field):
        return field.lower().strip() in bibpy.fields.all

    def validate_entry(entry):
        return entry.lower().strip() in bibpy.entries.all

    return base_parser(validate_field, validate_entry)


def relaxed_parser():
    """Return a grammar for a relaxed parser."""
    regex = r'[\w\-:\.]+'

    def validate_field(field):
        return re.match(regex, field.strip().lower())

    def validate_entry(entry):
        return re.match(regex, entry.strip().lower())

    return base_parser(validate_field, validate_entry)


def date_parser():
    """Return a parser for biblatex dates."""
    dash = skip('dash')
    forward_slash = token_type('slash')
    year = if_token_type('number', lambda v: len(v) == 4) >> token_value
    month = if_token_type('number', lambda v: len(v) == 2) >> token_value
    day = month
    date = year + parser.maybe(dash + month) + parser.maybe(dash + day)

    return date\
        + parser.maybe((forward_slash + date) | forward_slash)\
        + parser.skip(parser.finished)\
        >> make_date


def parse(string, format, ignore_comments=True):
    """Parse string using a given reference format."""
    grammar = grammar_from_format(format)

    try:
        strings, preambles, comment_entries, comments, entries =\
            [], [], [], [], []

        for result in grammar.parse(list(bibpy.lexers.lex_bib(string))):
            et = getattr(result, 'bibtype', False)

            if et == 'string':
                strings.append(result)
            elif et == 'comment':
                comment_entries.append(result)
            elif et == 'preamble':
                preambles.append(result)
            elif et:
                entries.append(result)
            else:
                if not ignore_comments and not re.match(r'^\s*$', result):
                    comments.append(result)

        return bibpy.entries.Entries(
            entries,
            strings,
            preambles,
            comment_entries,
            comments
        )
    except lexer.LexerError as ex:
        raise bibpy.error.LexerException(str(ex))
    except parser.NoParseError as ex:
        raise bibpy.error.ParseException(str(ex))


def parse_file(source, format, ignore_comments=True):
    """Parse a file using a given reference format."""
    with source:
        return parse(source.read(), format, ignore_comments)


def parse_date(datestring):
    """Parse a biblatex date."""
    grammar = grammar_from_format('date')

    try:
        return grammar.parse(list(bibpy.lexers.lex_date(datestring)))
    except lexer.LexerError as ex:
        raise bibpy.error.LexerException(str(ex))
    except parser.NoParseError as ex:
        raise bibpy.error.ParseException(str(ex))


def parse_string_expr(expr):
    """Parse a bibtex string expression."""
    if not expr:
        return expr

    return bibpy.lexers.lex_string_expr(expr)


def parse_braced_expr(expr):
    """Parse a braced string and return its tokens."""
    return [token.value for token in bibpy.lexers.lex_braced_expr(expr)]


def prefix_indices(parts):
    """Find the indices for a name prefix ('von' part) in a list of tokens."""
    i, j = -1, -1

    for k, p in enumerate(parts):
        if p.value.islower() and p.type != 'braced':
            i = k
            break

    if i != -1:
        j = i + 1

        for k in range(i + 1, len(parts) - 1):
            if parts[k].value.islower() and parts[k].type != 'braced':
                j = k + 1

    return i, j if j < len(parts) else j - 1


def parse_name(name):
    """Parse a name, such as an author."""
    if not name:
        return Name()

    first, prefix, last, suffix = '', '', '', ''
    tokens, commas = bibpy.lexers.lex_name(name)
    tokens = [token.value for token in tokens]
    stripped_tokens = [[token.value for token in part] for part in tokens]

    if commas == 0:
        # Assume 'first last' or 'first von last' format
        stripped_tokens = stripped_tokens[0]

        if len(stripped_tokens) == 1:
            last = stripped_tokens[0]
        else:
            pi = prefix_indices(tokens[0])

            if pi != (-1, -1):
                i, j = pi
                first = ' '.join(stripped_tokens[:i])
                prefix = ' '.join(stripped_tokens[i:j])
                last = ' '.join(stripped_tokens[j:])
            else:
                first = ' '.join(stripped_tokens[:-1])
                last = stripped_tokens[-1]
    elif commas == 1:
        # Assume 'von last, first' format
        pi = prefix_indices(tokens[0])

        if pi != (-1, -1):
            _, j = pi
            first = ' '.join(stripped_tokens[1])
            prefix = ' '.join(stripped_tokens[0][0:j])
            last = ' '.join(stripped_tokens[0][j:])
        else:
            first = ' '.join(stripped_tokens[1])
            last = ' '.join(stripped_tokens[0])
    elif commas >= 2:
        # Assume 'von last, jr, first' format
        pi = prefix_indices(tokens[0])

        if pi != (-1, -1):
            i, j = pi
            first = ' '.join(stripped_tokens[2])
            prefix = ' '.join(stripped_tokens[0][i:j])
            last = ' '.join(stripped_tokens[0][j:])
            suffix = ' '.join(stripped_tokens[1])
        else:
            first = ' '.join(stripped_tokens[2])
            last = ' '.join(stripped_tokens[0])
            suffix = ' '.join(stripped_tokens[1])

    return Name(first, prefix, last, suffix)


##################################################################
# Query Grammars
##################################################################
def make_query_result(query_type):
    """Return a function that creates the result of a query."""
    def _result(tokens):
        return (query_type, tokens)

    return _result


def key_query_parser():
    """Return a parser for key queries."""
    return (
        parser.maybe(token_type('not') | token_type('approx'))
        + token_type('name')
        + parser.skip(parser.finished)
    ) >> make_query_result('key')


def entry_query_parser():
    """Return a parser for name queries."""
    return (
        parser.maybe(token_type('not') | token_type('approx'))
        + token_type('name')
        + parser.skip(parser.finished)
    ) >> make_query_result('bibtype')


def field_query_parser():
    """Return a parser for numeric queries.

    Example queries: '1900-1995' or '>= 1998'

    """
    number = token_type('number')
    field_name = token_type('name')
    lt = token_type('lt')
    le = token_type('le')
    gt = token_type('gt')
    ge = token_type('ge')
    eq = token_type('equals')
    approx = token_type('approx')

    # Simple comparisons
    # NOTE: We put le before lt to parse both
    comparison = parser.maybe(token_type('not'))\
        + field_name\
        + (le | lt | ge | gt)\
        + number

    # Values can be given as intervals ('1990-2000')
    interval = parser.maybe(token_type('not'))\
        + field_name\
        + skip('equals')\
        + number\
        + skip('dash')\
        + number

    # Values can be given as ranges ('1990<=year<=2000')
    # NOTE: We put le before lt to parse both
    range_ = parser.maybe(token_type('not'))\
        + number\
        + (le | lt)\
        + field_name\
        + (le | lt)\
        + number

    # Field value queries ('year=2000' or 'author~Augustus')
    field_value = parser.maybe(token_type('not'))\
        + field_name\
        + (eq | approx)\
        + (token_type('name') | token_type('number') | token_type('any'))

    # Field occurrence ('publisher' or '^publisher')
    field_occurrence = parser.maybe(token_type('not')) + field_name

    return (interval >> make_query_result('interval')
            | comparison >> make_query_result('comparison')
            | range_ >> make_query_result('range')
            | field_value >> make_query_result('value')
            | field_occurrence >> make_query_result('occurrence'))\
        + parser.skip(parser.finished)


_query_grammars = {
    'bibkey':  key_query_parser(),
    'bibtype': entry_query_parser(),
    'field':   field_query_parser(),
}


def parse_query(query, query_type):
    """Parse a query and return the operator and value.

    E.g. '~Author' is parsed as ('~', 'Author')

    """
    try:
        tokens = bibpy.lexers.lex_generic_query(query)

        return _query_grammars[query_type].parse(tokens)
    except (lexer.LexerError, parser.NoParseError) as ex:
        raise bibpy.error.ParseException(
            'Error: One or more constraints failed to parse at column {0}'
            .format(ex.state.pos)
        )


##################################################################
# Top-level Grammars
##################################################################
# Convenience dictionary for selecting reference formats
_formats = {
    'bibtex':   bibtex_parser(),
    'biblatex': biblatex_parser(),
    'mixed':    mixed_parser(),
    'relaxed':  relaxed_parser(),
    'date':     date_parser()
}


def grammar_from_format(format):
    """Return the grammar correspoding to the given format string."""
    if format not in _formats:
        raise KeyError(
            "Reference format '{0}' does not exist (use any of {1})"
            .format(
                format,
                ", ".join(sorted(_formats.keys()))
            )
        )

    return _formats[format]
