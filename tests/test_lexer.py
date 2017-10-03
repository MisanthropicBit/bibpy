# -*- coding: utf-8 -*-

"""Test the lexer."""

from bibpy.lexers.biblexer import BibLexer


def token_types(tokens):
    return [token.type for token in tokens]


def test_lex_entry_no_fields():
    assert token_types(BibLexer().lex('@entry{key,}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma', 'rbrace']


def test_lex_entry_with_fields():
    assert token_types(BibLexer().lex('@entry{key,author ={bib}}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma',
         'name', 'equals', 'lbrace', 'content', 'rbrace', 'rbrace']


def test_lex_string_entry():
    assert token_types(BibLexer().lex('@string{variable = value }')) ==\
        ['entry', 'name', 'lbrace', 'name', 'equals', 'name', 'rbrace']

    assert token_types(BibLexer().lex('@string(variable = value )')) ==\
        ['entry', 'name', 'lparen', 'name', 'equals', 'name', 'rparen']


def test_lex_preamble_entry():
    assert token_types(BibLexer().lex('@preamble{Bla bla bla}')) ==\
        ['entry', 'name', 'lbrace', 'content', 'rbrace']

    assert token_types(BibLexer().lex('@preamble(Bla bla bla)')) ==\
        ['entry', 'name', 'lparen', 'content', 'rparen']


def test_lex_comment_entry():
    assert token_types(BibLexer().lex('@comment{Bla bla bla}')) ==\
        ['entry', 'name', 'lbrace', 'content', 'rbrace']

    assert token_types(BibLexer().lex('@comment(Bla bla bla)')) ==\
        ['entry', 'name', 'lparen', 'content', 'rparen']


def test_lex_with_comments():
    string = """This is a comment
@entry{
    key,
    year = 2001,
}

This is another"""

    assert token_types(BibLexer().lex(string)) ==\
        ['comment', 'entry', 'name', 'lbrace', 'name', 'comma', 'name',
         'equals', 'number', 'comma', 'rbrace', 'comment']
