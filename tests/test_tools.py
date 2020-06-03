# -*- coding: utf-8 -*-

"""Test the functions in the tools file."""

from bibpy.error import ParseException
from bibpy.parser import parse_query
import bibpy.tools
from io import StringIO
import pytest
from contextlib import redirect_stdout, redirect_stderr
import os


def test_version_format():
    assert bibpy.tools.format_version('0.1.0') == '%(prog)s v0.1.0'

    program_name = dict(prog='tool_name')

    assert bibpy.tools.format_version('2.3') % program_name == 'tool_name v2.3'


def test_key_grammar():
    assert parse_query('SomeKey', 'bibkey') == ('key', (None, 'SomeKey'))
    assert parse_query('^SomeKey', 'bibkey') == ('key', ('^', 'SomeKey'))

    with pytest.raises(ParseException):
        parse_query('?key', 'bibkey')


def test_entry_grammar():
    assert parse_query('article', 'bibtype') == ('bibtype', (None, 'article'))
    assert parse_query('^book', 'bibtype') == ('bibtype', ('^', 'book'))


# NOTE: We also test the numeric grammar here as it is part of the field query
# grammar
def test_field_grammar():
    assert parse_query('year<2000', 'field') ==\
        ('comparison', (None, 'year', '<', '2000'))
    assert parse_query('^year>2000', 'field') ==\
        ('comparison', ('^', 'year', '>', '2000'))
    assert parse_query('issue<=10', 'field') ==\
        ('comparison', (None, 'issue', '<=', '10'))
    assert parse_query('volume>100', 'field') ==\
        ('comparison', (None, 'volume', '>', '100'))
    assert parse_query('month>=9', 'field') ==\
        ('comparison', (None, 'month', '>=', '9'))
    assert parse_query('year=1990-2000', 'field') ==\
        ('interval', (None, 'year', '1990', '2000'))
    assert parse_query('1900 < year <= 2000', 'field') ==\
        ('range', (None, '1900', '<', 'year', '<=', '2000'))

    # Test invalid queries
    invalid_queries = [
        '!author .',         # Extra characters at the end
        'volume/1900-2000',  # '=' replaces by forward slash
        'author<>10',        # Invalid comparison operator
        'institution~'       # No value following '~'
    ]

    for query in invalid_queries:
        with pytest.raises(bibpy.error.ParseException):
            parse_query(query, 'field')


def test_predicate_composition():
    at = bibpy.tools.always_true
    af = bibpy.tools.always_false

    pred1 = bibpy.tools.compose_predicates([af, at, af], any)
    pred2 = bibpy.tools.compose_predicates([af, af, af], any)
    pred3 = bibpy.tools.compose_predicates([af, at], all)
    pred4 = bibpy.tools.compose_predicates([at, at], all)

    assert pred1(1)
    assert not pred2(1)
    assert not pred3(1)
    assert pred4(1)


def test_iter_files():
    assert set(bibpy.tools.iter_files(['bibpy/scripts'], 'bib*.py', True)) ==\
        set([
            'bibpy/scripts/bibstats.py',
            'bibpy/scripts/bibgrep.py',
            'bibpy/scripts/bibformat.py'
        ])

    assert set(bibpy.tools.iter_files(
        ['bibpy/scripts/bibstats.py'],
        'bib*',
        False
    )) == set(['bibpy/scripts/bibstats.py'])

    with pytest.raises(SystemExit):
        list(bibpy.tools.iter_files(['bibpy/scripts'], 'bib*', False))


def test_close_output_handles():
    sio1 = StringIO()
    sio2 = StringIO()

    with redirect_stdout(sio1) as stdout, redirect_stderr(sio2) as stderr:
        assert not stdout.closed
        assert not stderr.closed

        bibpy.tools.close_output_handles()

        assert stdout.closed
        assert stderr.closed


def test_get_abspath_for():
    path = bibpy.tools.get_abspath_for(__file__, 'test_tools.py')
    dir_path, file_path = os.path.split(path)

    assert os.path.dirname(__file__) == dir_path
    assert file_path == 'test_tools.py'
