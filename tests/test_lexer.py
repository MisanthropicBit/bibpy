# -*- coding: utf-8 -*-

"""Test the bib lexer."""

import bibpy
from bibpy.lexers.base_lexer import LexerError
from bibpy.lexers.biblexer import BibLexer
from bibpy.lexers.namelist_lexer import NamelistLexer
import pytest


def token_types(tokens):
    return [token.type for token in tokens]


def test_lex_entry_no_fields():
    assert token_types(BibLexer().lex('@entry{key,}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma', 'rbrace']


def test_lex_entry_with_fields():
    assert token_types(BibLexer().lex('@entry{key,author ={bib}}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma',
         'name', 'equals', 'lbrace', 'content', 'rbrace', 'rbrace']


def test_lex_string_field():
    assert token_types(BibLexer().lex('@entry{key,author = "bib"}')) ==\
        ['entry', 'name', 'lbrace', 'name', 'comma', 'name', 'equals',
         'string', 'rbrace']


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

    assert token_types(BibLexer().lex('@preamble((nested parentheses))')) ==\
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


def test_namelist_lexer():
    test1 = "T. Ohtsuki and H. Mori and T. Kashiwabara and T. Fujisawa"
    test2 = "T. Ohtsuki and H. Moriand and T. Kashiwabara and T. Fujisawa"
    test3 = "L. {Sunil Chandran} and C. R. Subramanian"
    test4 = "L. {Sunil Chandran} {and } C. R. Subramanian"

    assert list(NamelistLexer().lex(test1)) ==\
        ['T. Ohtsuki', 'H. Mori', 'T. Kashiwabara', 'T. Fujisawa']

    assert list(NamelistLexer().lex(test2)) ==\
        ['T. Ohtsuki', 'H. Moriand', 'T. Kashiwabara', 'T. Fujisawa']

    assert list(NamelistLexer().lex(test3)) ==\
        ['L. {Sunil Chandran}', 'C. R. Subramanian']

    assert list(NamelistLexer().lex(test4)) ==\
        ['L. {Sunil Chandran} {and } C. R. Subramanian']

    with pytest.raises(LexerError):
        list(NamelistLexer().lex('T. Ohtsuki and H. Mori and T. Kas}hiwabara'))


def test_lexer_fail():
    with pytest.raises(LexerError):
        list(BibLexer().lex('@entry!{key,author} ={bib}}'))

    with pytest.raises(LexerError):
        list(BibLexer().lex('@entrykey,author} = {bib}}'))
