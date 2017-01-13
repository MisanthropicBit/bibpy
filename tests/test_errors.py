"""Test expcetions."""

import bibpy
import bibpy.entry
import pytest


def test_required_field_error():
    entry = bibpy.entry.Entry('article', 'key')

    error1 = bibpy.error.RequiredFieldError(entry, ['article'], [])
    assert str(error1) == "Entry 'key' (type 'article') is missing " +\
                          "required field(s): article"

    error2 = bibpy.error.RequiredFieldError(entry, [], [['year', 'date']])
    assert str(error2) == "Entry 'key' (type 'article') is missing " +\
                          "required field(s): year/date"

    error3 = bibpy.error.RequiredFieldError(entry, ['title'],
                                            [['year', 'date']])
    assert str(error3) == "Entry 'key' (type 'article') is missing " +\
                          "required field(s): title, year/date"

    with pytest.raises(ValueError):
        bibpy.error.RequiredFieldError('key', [], [['year', 'date'],
                                                   ['editor']])
