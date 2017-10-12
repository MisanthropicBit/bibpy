# -*- coding: utf-8 -*-

"""Attempt to import a supported parser."""

import importlib


# Try funcparserlib first because the current implementation is fastest
_parser_abbreviations = [
    ('funcparserlib', 'fpl'),
    ('pyparsing', 'pp'),
]

for parserlib, abbrev in _parser_abbreviations:
    try:
        pmod = importlib.import_module('bibpy.parsers.{0}_parser'
                                       .format(abbrev))

        # Set parser functions
        parse = pmod.parse
        parse_file = pmod.parse_file
        parse_date = pmod.parse_date
        parse_string_expr = pmod.parse_string_expr
        parse_braced_expr = pmod.parse_braced_expr
        parse_query = pmod.parse_query

        break
    except AttributeError:
        pass  # Ignore parser if not all functions are implemented
    except ImportError:
        pass
else:
    raise ImportError("None of the supported parsers exist on this system "
                      "(attempted: {0})"
                      .format(", ".join(p for p, _ in _parser_abbreviations)))
