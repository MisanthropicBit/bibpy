"""Test the functions in the tools file."""

import bibpy.tools
# import pytest


def test_version_format():
    assert bibpy.tools.version_format().format('0.1.0') == '%(prog)s v0.1.0'

    program_name = dict(prog='tool_name')
    assert (bibpy.tools.version_format() % program_name).format('2.3') ==\
        'tool_name v2.3'


# TODO: Expand grammar tests with failures
def test_key_grammar():
    assert bibpy.tools.parse_query('SomeKey', 'entry_key') ==\
        ('key', ['', 'SomeKey'])
    assert bibpy.tools.parse_query('!SomeKey', 'entry_key') ==\
        ('key', ['!', 'SomeKey'])
    assert bibpy.tools.parse_query('~SomeKey', 'entry_key') ==\
        ('key', ['~', 'SomeKey'])


def test_entry_grammar():
    assert bibpy.tools.parse_query('article', 'entry_type') ==\
        ('entry', ['', 'article'])
    assert bibpy.tools.parse_query('!book', 'entry_type') ==\
        ('entry', ['!', 'book'])
    assert bibpy.tools.parse_query('~conference', 'entry_type') ==\
        ('entry', ['~', 'conference'])


def test_field_grammar():
    assert bibpy.tools.parse_query('year<2000', 'field') ==\
        ('comparison', ['year', '<', '2000'])
    assert bibpy.tools.parse_query('issue<=10', 'field') ==\
        ('comparison', ['issue', '<=', '10'])
    assert bibpy.tools.parse_query('volume>100', 'field') ==\
        ('comparison', ['volume', '>', '100'])
    assert bibpy.tools.parse_query('month>=9', 'field') ==\
        ('comparison', ['month', '>=', '9'])
    # assert bibpy.tools.parse_query('year=1990-2000', 'field') ==\
    #     ('interval', ['year', '1900', '2000'])
    # assert bibpy.tools.parse_query('1990 < year <= 2000', 'field') ==\
    #     ('range', ['1900', 'year', '2000'])


def test_numeric_grammar():
    pass


# def test_parse_query():
#     assert bibpy.tools.parse_query('~Author') == ('entry', ['~', 'Author'])
#     assert bibpy.tools.parse_query('!Author') == ('entry', ['!', 'Author'])

#     invalid_queries = [
#         '!author .',         # Extra characters at the end
#         'volume/1900-2000',  # '=' replaces by forward slash
#         'author<>10',        # Invalid comparison operator
#         'institution~'       # No value following '~'
#     ]

#     for query in invalid_queries:
#         with pytest.raises(bibpy.error.ParseException):
#             bibpy.tools.parse_query(query)


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
