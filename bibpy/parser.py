# -*- coding: utf-8 -*-

"""Attempt to import a supported parser."""


_ERR_MSG = "None of the supported parsers exist on this system "\
           "(attempted: {0})".format(", ".join('funcparserlib, pyparsing'))


try:
    # Try funcparserlib first because the current implementation is fastest
    from bibpy.parsers.fpl_parser import parse, parse_file, parse_date,\
        parse_string_expr, parse_braced_expr, parse_query
except ImportError:
    try:
        from bibpy.parsers.pp_parser import parse, parse_file, parse_date,\
            parse_string_expr, parse_braced_string_expr
    except ImportError:
        raise ImportError(_ERR_MSG)
