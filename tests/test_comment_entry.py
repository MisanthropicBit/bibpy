"""Test the comment entry."""

import bibpy
import bibpy.entry
import pytest


@pytest.fixture
def test_entries():
    entry1 = bibpy.entry.Comment('This is a comment')
    entry2 = bibpy.entry.Comment('This is also a comment')

    return entry1, entry2


def test_formatting(test_entries):
    entry = test_entries[0]

    assert str(entry) == "@comment{This is a comment}"
    assert entry.format() == "@comment{This is a comment}"
    assert entry.format(braces=False) == "@comment(This is a comment)"
    assert entry.format(indent='') == "@comment{This is a comment}"
    assert entry.format() == """@comment{This is a comment}"""
    assert entry.format(indent='', braces=False) ==\
        "@comment(This is a comment)"


def test_properties(test_entries):
    entry = test_entries[0]

    assert entry.bibtype == 'comment'
    assert entry.bibkey is None
    assert entry.fields == []
    assert entry == entry
    assert entry != test_entries[1]
    assert 'is' in entry
    assert 'lol' not in entry
    assert entry.valid('bibtex')
    assert not entry.valid('biblatex')
    assert not entry.valid('mixed')
    assert not entry.valid('relaxed')
    assert not entry.valid('kbsrgo')
    assert len(entry) == 1
    assert repr(entry) == "Comment(value=\"This is a comment\")"
    assert list(iter(entry)) == [(None, 'This is a comment')]

    with pytest.raises(AttributeError):
        entry['a']
