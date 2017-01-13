"""Test aliases for all entry classes."""

import bibpy
import bibpy.entry
import pytest


def test_aliases():
    assert bibpy.entries.aliases('inproceedings', 'biblatex') ==\
        ['conference']
    assert bibpy.entries.aliases('online', 'biblatex') == ['electronic', 'www']
    assert bibpy.entries.aliases('thesis', 'biblatex') ==\
        ['masterthesis', 'phdthesis']
    assert bibpy.entries.aliases('report', 'biblatex') == ['techreport']

    no_aliases = bibpy.entries.all\
        - set(bibpy.entries.biblatex_entry_type_aliases)

    for t in no_aliases:
        # There are no aliases in bibtex
        assert bibpy.entries.aliases(t, 'bibtex') == []
        assert bibpy.entries.aliases(t, 'biblatex') == []


def test_base_entry_aliases():
    with pytest.raises(NotImplementedError):
        be = bibpy.entry.BaseEntry()
        be.aliases('bibtex')


def test_entry_aliases():
    entry = bibpy.entry.Entry('online', 'key')

    assert entry.aliases('bibtex') == []
    assert entry.aliases('biblatex') == ['electronic', 'www']


def test_string_entry_aliases():
    assert bibpy.entry.String('variable', 'value').aliases('biblatex') == []


def test_preamble_entry_aliases():
    assert bibpy.entry.Preamble('code').aliases('stuff') == []


def test_comment_entry_aliases():
    assert bibpy.entry.Comment('comments!').aliases('') == []
