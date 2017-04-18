"""Test the functions in the tools file."""

import bibpy.tools


def test_version_format():
    assert bibpy.tools.version_format().format('0.1.0') == '%(prog)s v0.1.0'

    program_name = dict(prog='tool_name')
    assert (bibpy.tools.version_format() % program_name).format('2.3') ==\
        'tool_name v2.3'


def test_key_grammar():
    pass


def test_entry_grammar():
    pass


def test_field_grammar():
    pass


def test_numeric_grammar():
    pass


def test_parse_query():
    assert bibpy.tools.parse_query('~Author') == ('entry', ['~', 'Author'])
    assert bibpy.tools.parse_query('!Author') == ('entry', ['!', 'Author'])




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
