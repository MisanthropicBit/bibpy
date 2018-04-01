"""Various lexer functions used by the funcparserlib parser."""

import funcparserlib.lexer as lexer
from bibpy.compat import u
from bibpy.lexers.biblexer import BibLexer
from bibpy.lexers.name_lexer import NameLexer
from bibpy.lexers.namelist_lexer import NamelistLexer


def remove_whitespace_tokens(tokens):
    """Remove any whitespace tokens from the given list of tokens."""
    return [token for token in tokens if token.type != 'space']


def lex_bib(string):
    """Return a generator of bib(la)tex tokens."""
    return remove_whitespace_tokens(BibLexer().lex(string))


def lex_date(date_string):
    """Return the biblatex date tokens in a string."""
    tokenizer = lexer.make_tokenizer([
        ('number', [u('[0-9]+')]),
        ('dash',   [u('-')]),
        ('slash',  [u('/')])
    ])

    return list(tokenizer(date_string))


def lex_string_expr(string):
    """Return the tokens in a string expression."""
    tokenizer = lexer.make_tokenizer([
        ('concat', [u('#')]),
        ('string', [u('"[^"]+"')]),
        ('name',   [u('[A-Za-z_][A-Za-z_0-9\-:?\'\.]*')]),
        ('space',  [u('[ \t\r\n]+')]),
    ])

    return remove_whitespace_tokens(tokenizer(string))


def lex_braced_expr(string):
    """Return the tokens in a braced expression."""
    tokenizer = lexer.make_tokenizer([
        ('lbrace',  [u('{')]),
        ('rbrace',  [u('}')]),
        ('content', [u('[^{}]+')]),
    ])

    return remove_whitespace_tokens(tokenizer(string))


def lex_namelist(string):
    """Lex a namelist delimited by 'and'."""
    return [token for token in NamelistLexer().lex(string) if token]


def lex_name(string):
    """Return a generator of bib(la)tex name tokens."""
    name_lexer = NameLexer()

    return [token.name for token in name_lexer.lex(string)], name_lexer.commas


def lex_generic_query(query):
    """Return the tokens in a query."""
    tokenizer = lexer.make_tokenizer([
        ('ops',    [u('[\^~]')]),
        ('equals', [u('=')]),
        ('le',     [u('<=')]),
        ('lt',     [u('<')]),
        ('ge',     [u('>=')]),
        ('gt',     [u('>')]),
        ('comma',  [u(',')]),
        ('dash',   [u('-')]),
        ('number', [u('-?(0|([1-9][0-9]*))')]),
        ('name',   [u('\w+')]),
        ('space',  [u('[ \t\r\n]+')]),
        ('any',    [u('.+?')])
    ])

    return remove_whitespace_tokens(tokenizer(query))
