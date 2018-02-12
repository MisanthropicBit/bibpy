"""Test the preamble entry."""

import bibpy
import bibpy.entry
import pytest


@pytest.fixture
def test_entry():
    contents = 'LaTeX $\\textbf{code} $1$'

    return contents, bibpy.entry.Preamble(contents)


def test_formatting(test_entry):
    contents, entry = test_entry

    assert str(entry) == "@preamble{" + contents + "}"
    assert entry.format() == "@preamble{" + contents + "}"
    assert entry.format(braces=False) == "@preamble(" + contents + ")"
    assert entry.format(indent='') == "@preamble{" + contents + "}"
    assert entry.format(singleline=False) == """@preamble{
    """ + contents + """
}"""
    assert entry.format(singleline=False, indent='', braces=False) ==\
        """@preamble(
""" + contents + """
)"""


def test_properties(test_entry):
    contents, entry = test_entry

    assert entry.bibtype == 'preamble'
    assert entry.bibkey is None
    assert entry.fields == []
    assert entry == entry
    assert 'LaTeX' in entry
    assert 'lol' not in entry
    assert entry.valid('bibtex')
    assert not entry.valid('biblatex')
    assert not entry.valid('mixed')
    assert not entry.valid('relaxed')
    assert not entry.valid('olhisef')
    assert len(entry) == 1
    assert repr(entry) == "Preamble(value=\"" + contents + "\")"
    assert list(iter(entry)) == [(None, 'LaTeX $\\textbf{code} $1$')]

    with pytest.raises(AttributeError):
        entry['a']
