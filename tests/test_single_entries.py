"""Test parsing of single entries."""

import bibpy


def test_single_comment():
    s = "This is a comment"
    _, _, _, _, comments = bibpy.read_string(s, 'bibtex')

    assert comments[0] == s


def test_single_comment_entry():
    contents = "I can write whatever I want here"
    s = "@comment{ " + contents + " }"
    _, _, _, comment_entries, _ = bibpy.read_string(s, 'bibtex')

    assert type(comment_entries[0]) is bibpy.entry.Comment
    assert comment_entries[0].value == contents


def test_single_string_entry():
    variable = "var"
    value = "March"
    s = "@string{ " + variable + " = " + value + " }"
    _, strings, _, _, _ = bibpy.read_string(s, 'bibtex')

    assert type(strings[0]) is bibpy.entry.String
    assert strings[0].variable == variable
    assert strings[0].value == value


def test_single_preamble_entry():
    contents = "$1$ LaTeX code $\sqrt{2}"
    s = "@preamble( " + contents + " )"
    _, _, preambles, _, _ = bibpy.read_string(s, 'bibtex')

    assert type(preambles[0]) is bibpy.entry.Preamble
    assert preambles[0].value == contents


def test_single_entry():
    s = "@article{example_key,author={McLovin'}," +\
        "title={Hawaiian Organ Donation}}"

    entries, _, _, _, _ = bibpy.read_string(s, 'bibtex')

    assert type(entries[0]) is bibpy.entry.Entry
    assert entries[0].entry_type == 'article'
    assert entries[0].entry_key == 'example_key'
    assert entries[0].author == 'McLovin\''
    assert entries[0].title == 'Hawaiian Organ Donation'
