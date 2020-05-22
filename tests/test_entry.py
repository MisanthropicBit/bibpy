# -*- coding: utf-8 -*-

"""Test the entry class."""

import bibpy
import bibpy.entry
import pytest


@pytest.fixture
def test_entry():
    return bibpy.entry.Entry('article', 'key')


def test_formatting(test_entry):
    assert test_entry.format() == '@article{key,\n}'


def test_properties(test_entry):
    assert test_entry.bibtype == 'article'
    assert test_entry.bibkey == 'key'
    assert test_entry.aliases('bibtex') == []

    test_entry.author = 'Author'
    test_entry.title = 'Title'

    assert test_entry.get('author') == 'Author'
    assert test_entry.get('uobdrg', None) is None
    assert set(test_entry.keys()) == set(['author', 'title'])
    assert set(test_entry.values()) == set(['Author', 'Title'])

    test_entry.clear()

    assert not test_entry.fields
    assert test_entry.author is None
    assert test_entry.title is None

    test_entry.journaltitle = 'Journaltitle'
    assert test_entry.journaltitle == 'Journaltitle'
    del test_entry['journaltitle']
    assert test_entry.journaltitle is None

    assert not test_entry.valid('bibtex')
    assert not test_entry.valid('biblatex')
    assert test_entry.valid('relaxed')

    with pytest.raises(ValueError):
        test_entry.valid('seoligh')

    test_entry['author'] = 'Author'

    assert len(test_entry) == 1
    assert repr(test_entry) == "Entry(type=article, key=key)"
    assert test_entry['lhsfeslkj'] is None

    for fmt in ['bibtex', 'biblatex']:
        with pytest.raises(bibpy.error.RequiredFieldError):
            test_entry.validate(fmt)

    entry2 = bibpy.entry.Entry('manual', 'key2')
    assert test_entry != entry2

    # Entries are not equal to other types
    assert not entry2 == "Hello"

    # Entries must have the same entry type and key to be equal
    entry2.author = 'Johnson'
    test_entry.author = 'Johnson'
    assert test_entry != entry2

    entry2.bibtype = 'article'
    entry2.bibkey = 'key'
    entry2.author = 'Johnson'

    # Entries must have the same fields
    test_entry.author = 'Johnson'
    test_entry.year = 2007
    assert test_entry != entry2

    # Entries must have the same contents in their fields
    entry2.author = 'johnson'
    entry2.year = 2007
    assert test_entry != entry2
