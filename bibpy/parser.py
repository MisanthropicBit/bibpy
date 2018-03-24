"""Parsing functions using the funcparserlib library."""

import bibpy.compat
import bibpy.date
import bibpy.entry
import bibpy.lexers
from bibpy.compat import u
import funcparserlib.parser as parser
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
         enclosed('lparen', 'rparen', content)) >>\
        producer


def make_string(token):
    """Make a string from a token."""
    return token.value.strip()


def make_unquoted_string(token):
    """Remove double-quotes around a string and make a token."""
    return token.value.strip('"')


def make_variable(token):
    """Make a variable from a token."""
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

    return tokens[0].value +\
        "".join([getattr(t, 'content', t) for t in result]) +\
        tokens[2].value


def make_list(tokens):
    """Make a list from the list of parsed tokens."""
    return [tokens[0]] + tokens[1]


def make_field(tokens):
    """Make a field from two tokens."""
    return tokens[0].value.strip(), tokens[1]


def make_string_entry(tokens):
    """Make a bib string entry from a list of parsed tokens."""
    bibtype, [var, value] = tokens
    assert is_string_entry(bibtype.value)

    return bibpy.entry.String(var, value.strip('"'))


def make_comment_entry(tokens):
    """Make a comment entry from a list of parsed tokens."""
    bibtype, value = tokens
    assert is_comment_entry(bibtype.value)

    return bibpy.entry.Comment(value)


def make_preamble_entry(tokens):
    """Make a preamble entry from a list of parsed tokens."""
    bibtype, value = tokens
    assert is_preamble_entry(bibtype.value)

    return bibpy.entry.Preamble(value)


def make_entry(tokens):
    """Make a bib entry from a list of parsed tokens."""
    bibtype = tokens[0]
    bibkey = tokens[1]
    fields = tokens[2] if tokens[2] is not None else []

    return bibpy.entry.Entry(bibtype.lower(), bibkey,
                             fields=[(f.lower(), v) for f, v in fields])


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
    def _join_string_expr(tokens):
        if len(tokens) == 1:
            return tokens[0].strip('"')
        else:
            return delimiter.join(tokens)

    return _join_string_expr


def delimited_list(element, separator):
    """Create a parser of a list of delimited tokens."""
    return element + parser.many(parser.skip(token_type(separator)) + element)\
        >> make_list


def base_parser(validate_field, validate_entry):
    """Return the base parser which all other parsers are based on.

    The valid_fields and valid_entries arguments denote the allowable names for
    this grammar.

    """
    # Simple expressions
    integer = token_type('number')
    name = token_type('name')
    variable = name

    # Braced expressions e.g. '{braced}'
    # non_braced = if_token_type('name', lambda v: re.match('[^{}]+', v))
    non_braced = if_token_type('content', lambda v: True)
    braced_expr = parser.forward_decl()
    braced_expr.define(
        (if_token_type('lbrace', lambda v: True) +
         parser.many(braced_expr | non_braced) +
         if_token_type('rbrace', lambda v: True)) >> make_braced_expr
    )
    braced_expr = braced_expr >> remove_outer_braces

    # String expressions, e.g. '"This " # var # " that"'
    string_expr =\
        delimited_list(
            parser.some(lambda x: x.type == 'string') >> make_string |
            parser.some(lambda x: x.type == 'name') >> make_variable,
            'concat') >> join_string_expr(' # ')

    # The value of a field
    value = braced_expr | integer | variable | string_expr

    # Make sure we only parsed valid fields
    valid_field = if_token_type('name', validate_field)

    field = valid_field + skip('equals') + value >> make_field

    assignment = token_type('name') + skip('equals') + value

    # A regular comment: Any text outside of entries
    comment = token_type('comment')

    # @string
    string_entry = simple_entry(assignment, is_string_entry, make_string_entry)

    # @comment
    comment_entry = simple_entry(token_type('content'), is_comment_entry,
                                 make_comment_entry)

    # @preamble
    preamble_entry = simple_entry(token_type('content'), is_preamble_entry,
                                  make_preamble_entry)

    # Make sure we only parsed valid entries
    valid_entry = if_token_type('name', validate_entry) >> token_value

    # @article etc.
    entry = skip('entry') + valid_entry + skip('lbrace') +\
        token_type('name') + skip('comma') +\
        parser.maybe(delimited_list(field, 'comma')) +\
        parser.maybe(skip('comma')) +\
        skip('rbrace')\
        >> make_entry

    return parser.many(string_entry | comment_entry | preamble_entry |
                       entry | comment) + parser.skip(parser.finished)


def bibtex_parser():
    """Return a parser for bibtex."""
    def validate_field(field):
        return field.lower().strip() in bibpy.fields.bibtex

    def validate_entry(entry):
        return entry.lower().strip() in (bibpy.entries.bibtex |
                                         frozenset(['string', 'comment',
                                                    'preamble']))

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
    regex = u('[\w\-:\.]+')

    def validate_field(field):
        return re.match(regex, field, re.UNICODE)

    def validate_entry(entry):
        return re.match(regex, entry, re.UNICODE)

    return base_parser(validate_field, validate_entry)


def date_parser():
    """Return a parser for biblatex dates."""
    dash = skip('dash')
    forward_slash = token_type('slash')
    year = if_token_type('number', lambda v: len(v) == 4) >> token_value
    month = if_token_type('number', lambda v: len(v) == 2) >> token_value
    day = month
    date = year + parser.maybe(dash + month) + parser.maybe(dash + day)

    return date + parser.maybe((forward_slash + date) | forward_slash) +\
        parser.skip(parser.finished) >> make_date


def parse(string, format):
    """Parse string using a given reference format."""
    grammar = grammar_from_format(format)

    try:
        strings, preambles, comment_entries, comments, entries =\
            [], [], [], [], []

        for result in grammar.parse(bibpy.lexers.lex_bib(string)):
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
                if not re.match('^\s*$', result):
                    comments.append(result)

        return bibpy.entries.Entries(entries, strings, preambles,
                                     comment_entries, comments)
    except parser.NoParseError as e:
        raise bibpy.error.ParseException(bibpy.compat.u(str(e)))


def parse_file(source, format):
    """Parse a file using a given reference format."""
    try:
        with source:
            return parse(source.read(), format)
    except parser.NoParseError as e:
        raise bibpy.error.ParseException(str(e))


def parse_date(datestring):
    """Parse a biblatex date."""
    grammar = grammar_from_format('date')

    try:
        return grammar.parse(bibpy.lexers.lex_date(datestring))
    except parser.NoParseError as e:
        raise bibpy.error.ParseException(str(e))


def parse_string_expr(expr):
    """Parse a bibtex string expression."""
    if not expr:
        return expr

    # TODO: Test '"test #" # var'
    string_expr =\
        delimited_list(
            parser.some(lambda x: x.type == 'string') >> make_unquoted_string |
            parser.some(lambda x: x.type == 'name') >> token_value,
            'concat')

    try:
        tokens = bibpy.lexers.lex_string_expr(expr)

        if 'concat' not in (token.type for token in tokens):
            # Expression did not include any variable concatenations, so just
            # return it
            return expr
        else:
            return string_expr.parse(tokens)
    except parser.NoParseError:
        return expr


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
        return bibpy.name.Name()

    first, prefix, last, suffix = u'', u'', u'', u''
    tokens, commas = bibpy.lexers.lex_name(name)
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
                first = " ".join(stripped_tokens[:i])
                prefix = " ".join(stripped_tokens[i:j])
                last = " ".join(stripped_tokens[j:])
            else:
                first = " ".join(stripped_tokens[:-1])
                last = stripped_tokens[-1]
    elif commas == 1:
        # Assume 'von last, first' format
        pi = prefix_indices(tokens[0])

        if pi != (-1, -1):
            _, j = pi
            first = " ".join(stripped_tokens[1])
            prefix = " ".join(stripped_tokens[0][0:j])
            last = " ".join(stripped_tokens[0][j:])
        else:
            first = " ".join(stripped_tokens[1])
            last = " ".join(stripped_tokens[0])
    elif commas >= 2:
        # Assume 'von last, jr, first' format
        pi = prefix_indices(tokens[0])

        if pi != (-1, -1):
            i, j = pi
            first = " ".join(stripped_tokens[2])
            prefix = " ".join(stripped_tokens[0][i:j])
            last = " ".join(stripped_tokens[0][j:])
            suffix = " ".join(stripped_tokens[1])
        else:
            first = " ".join(stripped_tokens[2])
            last = " ".join(stripped_tokens[0])
            suffix = " ".join(stripped_tokens[1])

    return bibpy.name.Name(first, prefix, last, suffix)


##################################################################
# Query Grammars
##################################################################
def make_query_result(query_type):
    def _result(tokens):
        return (query_type, tokens)

    return _result


def key_query_parser():
    """Return a parser for key queries."""
    return (parser.maybe(token_type('ops')) + token_type('name') +
            parser.skip(parser.finished)) >> make_query_result('key')


def entry_query_parser():
    """Return a parser for name queries."""
    return (parser.maybe(token_type('ops')) + token_type('name') +
            parser.skip(parser.finished)) >> make_query_result('bibtype')


def field_query_parser():
    """Return a parser for field queries."""
    field_value = token_type('ops') + token_type('name') +\
        (token_type('equals') | token_type('tilde')) + token_type('any')

    field_occurrence = delimited_list(parser.maybe(token_type('ops')) +
                                      token_type('name'), 'comma')

    return (field_value | field_occurrence) + parser.skip(parser.finished)


def numeric_query_parser():
    """Return a parser for numeric queries.

    Example queries: '1900-1995' or '>= 1998'

    """
    integer = token_type('number')
    field_name = token_type('name')
    lt = token_type('lt')
    le = token_type('le')
    gt = token_type('gt')
    ge = token_type('ge')

    # Simple comparisons
    # NOTE: We put le before lt to parse both
    comparison = parser.maybe(token_type('ops')) + field_name +\
        (le | lt | ge | gt) + integer

    # Values can be given as intervals ('1990-2000')
    interval = parser.maybe(token_type('ops')) + field_name +\
        skip('equals') + integer + skip('dash') + integer

    # Values can be given as ranges ('1990<=year<=2000')
    # NOTE: We put le before lt to parse both
    range_ = parser.maybe(token_type('ops')) + integer + (le | lt) +\
        field_name + (le | lt) + integer

    return (interval >> make_query_result('interval') |
            comparison >> make_query_result('comparison') |
            range_ >> make_query_result('range')) +\
        parser.skip(parser.finished)


_query_grammars = {
    'bibkey':  key_query_parser(),
    'bibtype': entry_query_parser(),
    'field':   numeric_query_parser()
}


def parse_query(query, query_type):
    """Parse a query and return the operator and value.

    E.g. '~Author' is parsed as ('~', 'Author')

    """
    try:
        tokens = bibpy.lexers.lex_generic_query(query)

        return _query_grammars[query_type].parse(tokens)
    except parser.NoParseError as e:
        raise bibpy.error.ParseException("Error: One or more constraints "
                                         "failed to parse at column {0}"
                                         .format(e.state.pos))


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
        raise KeyError("Reference format '" + format + "' does not exist "
                       "(use any of " + ", ".join(sorted(_formats.keys())) +
                       ")")

    return _formats[format]
