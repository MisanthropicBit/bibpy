# -*- coding: utf-8 -*-

"""Test parsing of single entries."""

import bibpy
from bibpy.lexers.base_lexer import Token


def test_single_comment():
    s = 'This is a comment'
    comments = bibpy.read_string(s, 'bibtex', ignore_comments=False).comments

    assert comments[0] == s


def test_single_comment_entry():
    contents = ' I can write whatever I want here '
    s = '@comment{ I can write whatever I want here }'
    comment_entries = bibpy.read_string(s, 'bibtex').comment_entries

    assert type(comment_entries[0]) is bibpy.entry.Comment
    assert comment_entries[0].value == contents


def test_single_string_entry():
    variable = 'var'
    value = 'March'
    s = '@string{ ' + variable + ' = ' + value + ' }'
    strings = bibpy.read_string(s, 'bibtex').strings

    assert type(strings[0]) is bibpy.entry.String
    assert strings[0].variable == variable
    assert strings[0].value == value


def test_single_preamble_entry():
    contents = '$1$ LaTeX code $\\sqrt{2}'
    s = '@preamble( ' + contents + ' )'
    preambles = bibpy.read_string(s, 'bibtex').preambles

    assert type(preambles[0]) is bibpy.entry.Preamble
    assert preambles[0].value == contents


def test_single_capitalized_preamble_entry():
    contents = '$1$ LaTeX code $\\sqrt{2}'
    s = '@Preamble( ' + contents + ' )'
    preambles = bibpy.read_string(s, 'bibtex').preambles

    assert type(preambles[0]) is bibpy.entry.Preamble
    assert preambles[0].value == contents


def test_single_entry():
    s = "@article{example_key,author={McLovin'}," +\
        'title={Hawaiian Organ Donation}}'

    entries = bibpy.read_string(s, 'bibtex').entries

    assert type(entries[0]) is bibpy.entry.Entry
    assert entries[0].bibtype == 'article'
    assert entries[0].bibkey == 'example_key'
    assert entries[0].author == 'McLovin\''
    assert entries[0].title == 'Hawaiian Organ Donation'


def test_single_string_expr():
    s = 'var1 # " report on the " # Var_2 # " Conglomerate"'

    assert bibpy.parser.parse_string_expr(s) == [
        Token('name', 'var1 '),
        Token('concat', '#'),
        Token('string', '" report on the "'),
        Token('concat', '#'),
        Token('name', 'Var_2 '),
        Token('concat', '#'),
        Token('string', '" Conglomerate"')
    ]

    assert bibpy.parser.parse_string_expr('') == ''
