# -*- coding: utf-8 -*-

"""Test the string entry."""

import bibpy
import bibpy.entry
import pytest


@pytest.fixture
def test_entry():
    return bibpy.entry.String('variable', 'value')


def test_formatting(test_entry):
    assert str(test_entry) == '@string{variable = "value"}'
    assert test_entry.format() == '@string{variable = "value"}'
    assert test_entry.format(braces=False) == '@string(variable = "value")'
    assert test_entry.format(indent='') == '@string{variable = "value"}'
    assert test_entry.format(singleline=False) == """@string{
    variable = \"value\"
}"""
    assert test_entry.format(singleline=False, indent='', braces=False) ==\
        """@string(
variable = \"value\"
)"""


def test_properties(test_entry):
    assert test_entry.bibtype == 'string'
    assert test_entry.bibkey is None
    assert test_entry.fields == ['variable']
    assert test_entry.variable == 'variable'
    assert test_entry.value == 'value'
    assert test_entry.aliases('bibtex') == []
    assert test_entry.valid('bibtex')
    assert not test_entry.valid('biblatex')
    assert not test_entry.valid('mixed')
    assert not test_entry.valid('relaxed')
    assert not test_entry.valid('seoligh')
    assert 'variable' in test_entry
    assert 'missing' not in test_entry
    assert test_entry['variable'] == 'value'
    assert len(test_entry) == 1
    assert repr(test_entry) == 'String(variable = "value")'

    test_entry1 = bibpy.entry.String('variable', 'value')
    test_entry2 = bibpy.entry.String('a', '20')

    assert test_entry == test_entry1
    assert test_entry != test_entry2

    test_entry.variable = 'new'
    test_entry.value = 'Modified value'
    assert test_entry.variable == 'new'
    assert test_entry.value == 'Modified value'

    with pytest.raises(AttributeError):
        test_entry['lhsfeslkj']
