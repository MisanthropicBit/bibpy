"""Test the Entries class that contains results."""

import bibpy
import pytest


@pytest.fixture
def test_entries():
    return bibpy.read_file('tests/data/all_bibpy_entry_types.bib',
                           'relaxed')


def test_entries_properties(test_entries):
    comment_entry = bibpy.entry.Comment('Anything is possible with comments!')
    entry = bibpy.entry.Entry('unpublished', 'unpubkey',
                              **dict(author='Somebody McPerson',
                                     title='How To Parse BibTex',
                                     year='2011'))

    preamble_entry = bibpy.entry.Preamble('\\textbf{\\latex}')
    string_entry = bibpy.entry.String('variable', 'value')
    comment = 'This is just a comment'

    assert test_entries.comment_entries[0] == comment_entry
    assert test_entries.comments[0] == comment
    assert test_entries.entries[0] == entry
    assert test_entries.preambles[0] == preamble_entry
    assert test_entries.strings[0] == string_entry

    assert len(test_entries.all) == 4
    assert test_entries.all == [entry, string_entry, preamble_entry,
                                comment_entry]
