"""Test string variable expansion and unexpansion."""

import bibpy
import bibpy.entry
import pytest


@pytest.fixture
def test_entries():
    return bibpy.read_file('tests/data/string_variables.bib', 'bibtex')[:2]


def test_string_expand_start(test_entries):
    entries, strings = test_entries

    original_title = 'month # " Report"'
    entry = entries[0]
    assert entry.title == original_title

    bibpy.expand_strings([entry], strings)
    assert entry.title == 'March Report'

    bibpy.unexpand_strings([entry], strings)
    assert entry.title == original_title


def test_string_expand_middle(test_entries):
    entries, strings = test_entries

    original_title = '"Merci" # var # " Animals"'
    entry = entries[1]
    assert entry.title == original_title

    bibpy.expand_strings([entry], strings)
    assert entry.title == 'Merciless Animals'

    bibpy.unexpand_strings([entry], strings)
    assert entry.title == original_title


def test_string_expand_end(test_entries):
    entries, strings = test_entries

    original_author = '"Andre " # last_name'
    entry = entries[2]
    assert entry.author == original_author

    bibpy.expand_strings([entry], strings)
    assert entry.author == "Andre Cook"

    bibpy.unexpand_strings([entry], strings)
    assert entry.author == original_author


def test_string_expand_multiple(test_entries):
    entries, strings = test_entries

    original_institution = '"This " # var1 # " expand " # var2 # " variables"'
    entry = entries[3]
    assert entry.institution == original_institution

    bibpy.expand_strings([entry], strings)
    assert entry.institution == "This should expand multiple variables"

    bibpy.unexpand_strings([entry], strings)
    assert entry.institution == original_institution


def test_string_expand_none(test_entries):
    entries, strings = test_entries

    original_author = 'Regular Author'
    original_title = 'Regular Title'
    entry = entries[4]
    assert entry.author == original_author
    assert entry.title == original_title

    bibpy.expand_strings([entry], strings)
    assert entry.author == original_author
    assert entry.title == original_title

    bibpy.unexpand_strings([entry], strings)
    assert entry.author == original_author
    assert entry.title == original_title


def test_string_expand_empty(test_entries):
    entries, strings = test_entries

    string = [bibpy.entry.String('variable', 'value')]

    assert bibpy.expand_strings([], string) is None
    assert bibpy.expand_strings(entries[0], []) is None
    assert bibpy.unexpand_strings([], string) is None
    assert bibpy.unexpand_strings(entries[0], []) is None


def test_duplicate_string_variables(test_entries):
    entries, _ = test_entries
    strings = [bibpy.entry.String('var', '20'),
               bibpy.entry.String('var', '99')]

    with pytest.raises(ValueError):
        bibpy.expand_strings(entries, strings, ignore_duplicates=False)

    bibpy.expand_strings(entries, strings, ignore_duplicates=True)
    assert entries[1].title == "Merci99 Animals"

    with pytest.raises(ValueError):
        bibpy.unexpand_strings(entries, strings, ignore_duplicates=False)

    bibpy.unexpand_strings(entries, strings, ignore_duplicates=True)
