# -*- coding: utf-8 -*-

"""Test the lexer for lists of names."""

from bibpy.lexers.base_lexer import LexerError
from bibpy.lexers.namelist_lexer import NamelistLexer
import pytest


def test_namelist_lexer():
    test1 = 'T. Ohtsuki and H. Mori and T. Kashiwabara and T. Fujisawa'
    test2 = 'T. Ohtsuki and H. Moriand and T. Kashiwabara and T. Fujisawa'
    test3 = 'L. {Sunil Chandran} and C. R. Subramanian'
    test4 = 'L. {Sunil Chandran} {and } C. R. Subramanian'

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
