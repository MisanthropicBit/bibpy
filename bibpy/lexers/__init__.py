"""Various lexer functions used by the funcparserlib parser."""

import funcparserlib.lexer as lexer
from bibpy.lexers.biblexer import BibLexer


def lex_bib(string):
    """Return a generator of bib(la)tex tokens."""
    return [token for token in BibLexer().lex(string) if token != 'space']


def lex_date(date_string):
    """Return the biblatex date tokens in a string."""
    tokenizer = lexer.make_tokenizer([
        ('number', [u'[0-9]+']),
        ('dash',   [u'-']),
        ('slash',  [u'/'])
    ])

    return list(tokenizer(date_string))


def lex_string_expr(string):
    """Return the tokens in a string expression."""
    tokenizer = lexer.make_tokenizer([
        ('concat', [u'#']),
        ('string', [u'"[^"]+"']),
        ('name',   [u'[A-Za-z_][A-Za-z_0-9\-:?\'\.]*']),
        ('space',  [u'[ \t\r\n]+']),
    ])

    return [token for token in tokenizer(string) if token.type != 'space']


def lex_braced_expr(string):
    """Return the tokens in a braced expression."""
    tokenizer = lexer.make_tokenizer([
        ('lbrace',  [u'{']),
        ('rbrace',  [u'}']),
        ('content', [u'[^{}]+']),
    ])

    return [token for token in tokenizer(string) if token.type != 'space']


def lex_generic_query(query):
    """Return the tokens in a query."""
    tokenizer = lexer.make_tokenizer([
        ('ops',    [u'[\^~]']),
        ('equals', [u'=']),
        ('le',     [u'<=']),
        ('lt',     [u'<']),
        ('ge',     [u'>=']),
        ('gt',     [u'>']),
        ('comma',  [u',']),
        ('dash',   [u'-']),
        ('number', [u'-?(0|([1-9][0-9]*))']),
        ('name',   [u'\w+']),
        ('space',  [u'[ \t\r\n]+']),
        ('any',    [u'.+?'])
    ])

    return [token for token in tokenizer(query) if token.type != 'space']
