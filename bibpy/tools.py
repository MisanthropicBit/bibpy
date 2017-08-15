# -*- coding: utf-8 -*-

"""A collection of functionality for the tools in bin/.

This wraps the dependence on pyparsing in a module to make the bin tools more
maintainable.

"""

import bibpy.error
import pyparsing as pp


def version_format():
    """Return the version format used by bibpy's accompanying tools."""
    return '%(prog)s v{0}'


def always_true(value):
    """A function that always returns True."""
    return True


def always_false(value):
    """A function that always returns False."""
    return False


def key_grammar():
    """Return the grammar for parsing key queries."""
    return (pp.Combine(pp.Optional(pp.Literal('!')) +
                       pp.Optional(pp.Literal('~'))) +
            pp.Regex('.+'))('key')


def entry_grammar():
    """Return the grammar for parsing name queries."""
    return (pp.Combine(pp.Optional(pp.Literal('!')) +
                       pp.Optional(pp.Literal('~'))) +
            pp.Word(pp.alphas))('entry')


def field_grammar():
    """Return."""
    return (pp.Optional(pp.Literal('!')) + pp.Word(pp.alphas) +
            (pp.Literal('=') | pp.Literal('~')) + pp.Regex('.+'))('field')


def numeric_grammar():
    """Return the grammar for parsing year queries.

    Example queries are: '1900-1995' or '>= 1998'

    """
    integer = pp.Word(pp.nums)
    field_name = pp.Word(pp.alphas)  # pp.Regex('\w+')
    lt = pp.Literal('<')
    le = pp.Literal('<=')
    gt = pp.Literal('>')
    ge = pp.Literal('>=')

    # Simple comparisons
    # NOTE: We put le before lt to parse both
    comparison = (field_name + (le | lt | ge | gt) + integer)('comparison')

    # Values can be given as intervals ('1990-2000')
    interval = (field_name + pp.Literal('=') + integer + pp.Suppress('-') +
                integer)('interval')

    # Values can be given as ranges ('1990<=year<=2000')
    # NOTE: We put le before lt to parse both
    range_ = (integer + (le | lt) + field_name + (le | lt) + integer)('range')

    return interval | comparison | range_


_GRAMMARS = {
    'entry_key':  key_grammar(),
    'entry_type': entry_grammar(),
    'field':      field_grammar() | numeric_grammar()
}


def parse_query(query, query_type):
    """Parse a query and return the operator and value.

    E.g. '~Author' is parsed as ('~', 'Author')

    """
    try:
        result = _GRAMMARS[query_type].parseString(query, parseAll=True)

        return result.getName(), result.asList()
    except pp.ParseException as e:
        raise bibpy.error.ParseException("Error: One or more constraints "
                                         "failed to parse at column " +
                                         str(e.col))


def compose_predicates(predicates, pred_combiner):
    """Return a function that composes all the given predicates."""
    def composed_predicates(value):
        return pred_combiner(pred(value) for pred in predicates)

    return composed_predicates
