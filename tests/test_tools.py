# -*- coding: utf-8 -*-

"""Test the functions in the tools file."""

import bibpy.parser
import bibpy.tools
import pytest


def test_version_format():
    assert bibpy.tools.version_format().format('0.1.0') == '%(prog)s v0.1.0'

    program_name = dict(prog='tool_name')
    assert (bibpy.tools.version_format() % program_name).format('2.3') ==\
        'tool_name v2.3'


# TODO: Expand grammar tests with failures
def test_key_grammar():
    assert bibpy.parser.parse_query('SomeKey', 'bibkey') ==\
        ('key', (None, 'SomeKey'))
    assert bibpy.parser.parse_query('^SomeKey', 'bibkey') ==\
        ('key', ('^', 'SomeKey'))
    assert bibpy.parser.parse_query('~SomeKey', 'bibkey') ==\
        ('key', ('~', 'SomeKey'))


def test_entry_grammar():
    assert bibpy.parser.parse_query('article', 'bibtype') ==\
        ('bibtype', (None, 'article'))
    assert bibpy.parser.parse_query('^book', 'bibtype') ==\
        ('bibtype', ('^', 'book'))
    assert bibpy.parser.parse_query('~conference', 'bibtype') ==\
        ('bibtype', ('~', 'conference'))


# NOTE: We also test the numeric grammar here as it is part of the field query
# grammar
def test_field_grammar():
    assert bibpy.parser.parse_query('year<2000', 'field') ==\
        ('comparison', (None, 'year', '<', '2000'))
    assert bibpy.parser.parse_query('^year>2000', 'field') ==\
        ('comparison', ('^', 'year', '>', '2000'))
    assert bibpy.parser.parse_query('issue<=10', 'field') ==\
        ('comparison', (None, 'issue', '<=', '10'))
    assert bibpy.parser.parse_query('volume>100', 'field') ==\
        ('comparison', (None, 'volume', '>', '100'))
    assert bibpy.parser.parse_query('month>=9', 'field') ==\
        ('comparison', (None, 'month', '>=', '9'))
    assert bibpy.parser.parse_query('year=1990-2000', 'field') ==\
        ('interval', (None, 'year', '1990', '2000'))
    assert bibpy.parser.parse_query('1900 < year <= 2000', 'field') ==\
        ('range', (None, '1900', '<', 'year', '<=', '2000'))

    # Test invalid queries
    invalid_queries = [
        # '!author .',         # Extra characters at the end
        'volume/1900-2000',  # '=' replaces by forward slash
        'author<>10',        # Invalid comparison operator
        'institution~'       # No value following '~'
    ]

    for query in invalid_queries:
        with pytest.raises(bibpy.error.ParseException):
            bibpy.parser.parse_query(query, 'field')


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
