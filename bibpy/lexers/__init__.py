# -*- coding: utf-8 -*-

"""Various lexer functions used by the parsers."""

from bibpy.lexers.biblexer import BibLexer
from bibpy.lexers.name_lexer import NameLexer
from bibpy.lexers.namelist_lexer import NamelistLexer
import funcparserlib.lexer as lexer
from funcparserlib.lexer import Token


def remove_whitespace_tokens(tokens):
    """Remove any whitespace tokens from a list of tokens."""
    return [token for token in tokens if token.type != 'space']


def lex_bib(string):
    """Lex a string into bib tokens."""
    return BibLexer().lex(string)


def lex_date(date_string):
    """Lex a string into biblatex date tokens."""
    tokenizer = lexer.make_tokenizer([
        ('number', [r'[0-9]+']),
        ('dash',   [r'-']),
        ('slash',  [r'/'])
    ])

    return tokenizer(date_string)


def lex_string_expr(string):
    """Lex a string expression."""
    tokenizer = lexer.make_tokenizer([
        ('concat', [r'#']),
        ('string', [r'"[^"]+"']),
        ('name',   [r'[A-Za-z_][A-Za-z_0-9\-:?\'\.\s]*']),
        ('space',  [r'[ \t\r\n]+']),
    ])

    try:
        return remove_whitespace_tokens(tokenizer(string))
    except lexer.LexerError:
        # If we fail to lex the string, it is not a valid string expression so
        # just return it as a single token
        return [Token('string', string)]


def lex_braced_expr(string):
    """Lex a braced expression."""
    tokenizer = lexer.make_tokenizer([
        ('lbrace',  [r'{']),
        ('rbrace',  [r'}']),
        ('content', [r'[^{}]+']),
    ])

    return remove_whitespace_tokens(tokenizer(string))


def lex_namelist(string):
    """Lex a namelist delimited by zero brace-level 'and'."""
    return NamelistLexer().lex(string)


def lex_name(string):
    """Lex a name into parts."""
    name_lexer = NameLexer()

    # We have to force evaluation here so commas are also evaluated
    return list(name_lexer.lex(string)), name_lexer.commas


def lex_generic_query(query):
    """Lex a query string.

    Used by bibpy's accompanying tools.

    """
    tokenizer = lexer.make_tokenizer([
        ('not',    [r'\^']),
        ('equals', [r'=']),
        ('approx', [r'~']),
        ('le',     [r'<=']),
        ('lt',     [r'<']),
        ('ge',     [r'>=']),
        ('gt',     [r'>']),
        ('comma',  [r',']),
        ('dash',   [r'-']),
        ('number', [r'-?(0|([1-9][0-9]*))']),
        ('name',   [r'\w+']),
        ('space',  [r'[ \t\r\n]+']),
        ('any',    [r'[^<><=>=\s=\^~]+'])
    ])

    return remove_whitespace_tokens(tokenizer(query))
