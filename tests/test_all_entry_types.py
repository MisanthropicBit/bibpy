# -*- coding: utf-8 -*-

"""Ensure that all formats, apart from relaxed, can be parsed."""

import bibpy

filename = "tests/data/simple_1.bib"


def test_all_entry_types_bibtex():
    """Ensure that all bitex entry types can be parsed."""
    entries = bibpy.read_file(filename, 'bibtex').entries
    entry1 = entries[0]
    entry2 = entries[1]

    assert entry1.bibtype == 'article'
    assert entry1.bibkey == 'test'
    assert entry1.author == 'James Conway and Archer Sterling'
    assert entry1.title == '1337 Hacker'
    assert entry1.year == '2010'
    assert entry1.month == '4'
    assert entry1.institution == 'Office of Information Management {and} ' +\
                                 'Communications'

    assert entry2.bibtype == 'conference'
    assert entry2.bibkey == 'anything'
    assert entry2.author == 'k'


def test_all_entry_types_biblatex():
    """Ensure that all biblatex entry types can be parsed."""
    entries = bibpy.read_file(filename, 'bibtex').entries
    entry1 = entries[0]
    entry2 = entries[1]

    assert entry1.bibtype == 'article'
    assert entry1.bibkey == 'test'
    assert entry1.author == 'James Conway and Archer Sterling'
    assert entry1.title == '1337 Hacker'
    assert entry1.year == '2010'
    assert entry1.month == '4'
    assert entry1.institution == 'Office of Information Management {and} ' +\
                                 'Communications'

    assert entry2.bibtype == 'conference'
    assert entry2.bibkey == 'anything'
    assert entry2.author == 'k'


def test_all_entry_types_mixed():
    """Ensure that all mixed entry types can be parsed."""
    entries = bibpy.read_file(filename, 'mixed').entries
    print(entries)
    entry1 = entries[0]
    entry2 = entries[1]

    assert entry1.bibtype == 'article'
    assert entry1.bibkey == 'test'
    assert entry1.author == 'James Conway and Archer Sterling'
    assert entry1.title == '1337 Hacker'
    assert entry1.year == '2010'
    assert entry1.month == '4'
    assert entry1.institution == 'Office of Information Management {and} ' +\
                                 'Communications'

    assert entry2.bibtype == 'conference'
    assert entry2.bibkey == 'anything'
    assert entry2.author == 'k'
