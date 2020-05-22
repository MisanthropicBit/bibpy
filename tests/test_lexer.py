# -*- coding: utf-8 -*-

"""Test the bib lexer."""

from bibpy.lexers.base_lexer import LexerError
from bibpy.lexers.biblexer import BibLexer
import pytest


@pytest.fixture
def biblexer():
    return BibLexer()


def token_types(tokens):
    return [token.type for token in tokens]


def test_lex_entry_no_fields(biblexer):
    assert biblexer.current_char is None

    assert token_types(biblexer.lex('@entry{key,}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma', 'rbrace']


def test_lex_entry_with_fields(biblexer):
    assert token_types(biblexer.lex('@entry{key,author ={bib}}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma',
         'name', 'equals', 'lbrace', 'content', 'rbrace', 'rbrace']


def test_lex_string_field(biblexer):
    assert token_types(biblexer.lex('@entry{key,author = "bib"}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma', 'name', 'equals',
         'string', 'rbrace']


def test_lex_string_entry(biblexer):
    assert token_types(biblexer.lex('@string{variable = value }')) ==\
        ['entry', 'name', 'lbrace', 'name', 'equals', 'name', 'rbrace']

    assert token_types(biblexer.lex('@string(variable = value )')) ==\
        ['entry', 'name', 'lparen', 'name', 'equals', 'name', 'rparen']


def test_lex_preamble_entry(biblexer):
    assert token_types(biblexer.lex('@preamble{Bla bla bla}')) ==\
        ['entry', 'name', 'lbrace', 'content', 'rbrace']

    assert token_types(biblexer.lex('@preamble(Bla bla bla)')) ==\
        ['entry', 'name', 'lparen', 'content', 'rparen']

    assert token_types(biblexer.lex('@preamble((nested parentheses))')) ==\
        ['entry', 'name', 'lparen', 'content', 'rparen']


def test_lex_comment_entry(biblexer):
    assert token_types(biblexer.lex('@comment{Bla bla bla}')) ==\
        ['entry', 'name', 'lbrace', 'content', 'rbrace']

    assert token_types(biblexer.lex('@comment(Bla bla bla)')) ==\
        ['entry', 'name', 'lparen', 'content', 'rparen']


def test_lex_with_comments(biblexer):
    string = """This is a comment
@entry{
    key,
    year = 2001,
}

This is another"""

    assert token_types(biblexer.lex(string)) == [
        'comment',
        'entry',
        'name',
        'lbrace',
        'name',
        'comma',
        'name',
        'equals',
        'number',
        'comma',
        'rbrace',
        'comment',
    ]


def test_lexer_fail(biblexer):
    with pytest.raises(LexerError):
        list(biblexer.lex('@entry!{key,author} ={bib}}'))

    with pytest.raises(LexerError):
        list(biblexer.lex('@entrykey,author} = {bib}}'))

    with pytest.raises(LexerError) as exc_info:
        biblexer.reset('iojdogij rsoij oisjr')
        biblexer.expect('entry')

    assert exc_info.value.args[0] == "Did not find expected token 'entry'"
