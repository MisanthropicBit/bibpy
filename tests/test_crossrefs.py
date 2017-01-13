"""Test inheritance and uninheritance of crossreferences."""

import bibpy
import bibpy.entry
import pytest


@pytest.fixture
def test_entries():
    entry1 = bibpy.entry.Entry('inbook', 'key1',
                               **{'crossref': 'key2',
                                  'title':    'Title',
                                  'author':   'Author',
                                  'pages':    '5--25'})
    entry2 = bibpy.entry.Entry('book', 'key2',
                               **{'subtitle':  'Booksubtitle',
                                  'title':     'Booktitle',
                                  'author':    'Author2',
                                  'date':      '1995',
                                  'publisher': 'Publisher',
                                  'location':  'Location'})

    return [entry1, entry2]


def test_inheritance_no_override_no_exceptions(test_entries):
    bibpy.inherit_crossrefs(test_entries, inherit=True, override=False,
                            exceptions={})

    entry1 = test_entries[0]
    assert entry1.crossref == 'key2'
    assert entry1.title == 'Title'
    assert entry1.author == 'Author'
    assert entry1.booktitle == 'Booktitle'
    assert entry1.booksubtitle == 'Booksubtitle'


def test_inheritance_with_override_no_exceptions(test_entries):
    # Set the target entry's booktitle field
    test_entries[0].booktitle = 'Cool Booktitle'

    bibpy.inherit_crossrefs(test_entries, inherit=True, override=True,
                            exceptions={})

    entry1 = test_entries[0]
    assert entry1.crossref == 'key2'
    assert entry1.title == 'Title'
    assert entry1.author == 'Author'
    assert entry1.booktitle == 'Booktitle'
    assert entry1.booksubtitle == 'Booksubtitle'


def test_no_inheritance(test_entries):
    entry1, entry2 = test_entries
    bibpy.inherit_crossrefs(test_entries, inherit=False)

    assert set(entry1.fields) == set(['crossref', 'title', 'author', 'pages'])
    assert entry1.crossref == 'key2'
    assert entry1.title == 'Title'
    assert entry1.author == 'Author'
    assert entry1.pages == '5--25'

    assert set(entry2.fields) == set(['subtitle', 'title', 'author', 'date',
                                      'publisher', 'location'])
    assert entry2.subtitle == 'Booksubtitle'
    assert entry2.title == 'Booktitle'
    assert entry2.author == 'Author2'
    assert entry2.date == '1995'
    assert entry2.publisher == 'Publisher'
    assert entry2.location == 'Location'


def test_inheritance_with_exceptions(test_entries):
    exceptions = {('book', 'inbook'): {'inherit': False}}

    bibpy.inherit_crossrefs(test_entries, inherit=True, override=False,
                            exceptions=exceptions)

    entry1 = test_entries[0]
    assert entry1.crossref == 'key2'
    assert entry1.title == 'Title'
    assert entry1.author == 'Author'
    assert entry1.pages == '5--25'


def test_crossref_inheritance_with_exceptions(test_entries):
    exceptions = {('inbook', 'book'): {'inherit': False}}

    bibpy.inherit_crossrefs(test_entries, inherit=True, override=False,
                            exceptions=exceptions)

    entry1 = test_entries[0]
    assert entry1.crossref == 'key2'
    assert entry1.title == 'Title'
    assert entry1.author == 'Author'
    assert entry1.pages == '5--25'


def test_uninheritance_no_override(test_entries):
    bibpy.inherit_crossrefs(test_entries, inherit=True, override=False,
                            exceptions={})

    bibpy.uninherit_crossrefs(test_entries, inherit=True, override=False,
                              exceptions={})

    entry = test_entries[0]
    assert set(entry.fields) == set(['crossref', 'title', 'author', 'pages'])
    assert entry.crossref == 'key2'
    assert entry.title == 'Title'
    assert entry.booktitle is None
    assert entry.booksubtitle is None


def test_uninheritance_with_override(test_entries):
    bibpy.inherit_crossrefs(test_entries, inherit=True, override=False,
                            exceptions={})

    # NOTE: Does override even make sense here?
    bibpy.uninherit_crossrefs(test_entries, inherit=False, override=True,
                              exceptions={})

    # Should not change the entries as inherit is still False in
    # bibpy.uninherit_crossrefs
    entry1 = test_entries[0]
    assert entry1.crossref == 'key2'
    assert entry1.title == 'Title'
    assert entry1.author == 'Author'
    assert entry1.booktitle == 'Booktitle'
    assert entry1.booksubtitle == 'Booksubtitle'


def test_uninheritance_no_override_with_exceptions(test_entries):
    entry1, entry2 = test_entries

    bibpy.inherit_crossrefs(test_entries, inherit=True, override=False)

    # Do not uninherit fields in @books crossreferenceing @inbooks
    bibpy.uninherit_crossrefs(test_entries, exceptions={('inbook', 'book'):
                                                        {'inherit': False}})

    assert entry1.crossref == 'key2'
    assert entry1.title == 'Title'
    assert entry1.author == 'Author'
    assert entry1.booktitle == 'Booktitle'
    assert entry1.booksubtitle == 'Booksubtitle'
