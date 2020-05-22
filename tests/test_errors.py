# -*- coding: utf-8 -*-

"""Test expcetions."""

import bibpy
import bibpy.entry
import pytest


def test_lexer_error():
    error = bibpy.lexers.base_lexer.LexerError('msg', 20, 'a', 2, 1, 'a test')

    assert str(error) ==\
        "Failed at line 2, char 'a', position 20, brace level 1: msg"\
        " (line: 'a test')"


def test_required_field_error():
    entry = bibpy.entry.Entry('article', 'key')

    error1 = bibpy.error.RequiredFieldError(entry, ['article'], [])
    assert str(error1) == "Entry 'key' (type 'article') is missing " +\
                          "required field(s): article"

    error2 = bibpy.error.RequiredFieldError(entry, [], [['year', 'date']])
    assert str(error2) == "Entry 'key' (type 'article') is missing " +\
                          "required field(s): year/date"

    error3 = bibpy.error.RequiredFieldError(
        entry,
        ['title'],
        [['year', 'date']]
    )
    assert str(error3) == "Entry 'key' (type 'article') is missing " +\
                          "required field(s): title, year/date"

    assert error3.entry == entry
    assert error3.required == ['title']
    assert error3.optional == [['year', 'date']]

    with pytest.raises(ValueError):
        bibpy.error.RequiredFieldError(
            'key',
            [],
            [['year', 'date'], ['editor']],
        )
