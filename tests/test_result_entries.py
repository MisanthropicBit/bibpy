# -*- coding: utf-8 -*-

"""Test the Entries class that contains results."""

import bibpy
import pytest


@pytest.fixture
def test_entries():
    return bibpy.read_file(
        'tests/data/all_bibpy_entry_types.bib',
        ignore_comments=False
    )


def test_entries_properties(test_entries):
    comment_entry = bibpy.entry.Comment(
        '\n    Anything is possible with comments!\n'
    )
    entry = bibpy.entry.Entry(
        'unpublished',
        'unpubkey',
        **dict(
            author='Somebody McPerson',
            title='How To Parse BibTex',
            year='2011'
        )
    )

    preamble_entry = bibpy.entry.Preamble('\\textbf{\\latex}')
    string_entry = bibpy.entry.String('variable', 'value')
    comment = '\n\nThis is just a comment\n'

    assert test_entries.comment_entries[0] == comment_entry
    assert test_entries.comments[0] == comment
    assert test_entries.entries[0] == entry
    assert test_entries.preambles[0] == preamble_entry
    assert test_entries.strings[0] == string_entry

    assert len(test_entries.all_entries) == 4
    assert len(test_entries.all) == 5

    assert test_entries.all_entries == [
        [string_entry],
        [preamble_entry],
        [comment_entry],
        [entry]
    ]

    assert test_entries.all == [
        [string_entry],
        [preamble_entry],
        [comment_entry],
        [entry],
        [comment]
    ]

    assert list(iter(test_entries)) == [
        string_entry,
        preamble_entry,
        comment_entry,
        entry,
        comment
    ]

    assert test_entries[0] == [string_entry]
    assert test_entries[1] == [preamble_entry]
    assert test_entries[2] == [comment_entry]
    assert test_entries[3] == [entry]
    assert test_entries[4] == [comment]

    assert str(test_entries) == repr(test_entries)
    assert repr(test_entries) ==\
        'Entries(strings=1, preambles=1, comment_entries=1, entries=1)'
