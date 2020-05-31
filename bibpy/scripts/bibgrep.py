#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""bibgrep: Grep for bib(la)tex files.

To get all articles where the author contains 'Johnson' and the article is from
2010 or beyond:

>>> bibgrep --entry="article" --field="author~Johnson" --field="year>=2010"

The key, entry and field arguments take strings in a mini query language. For
keys and entries, the format is:

"[^][~]<key>"
"[^][~]<bibtype>"

where <key> is something like 'Johnson2002' and <bibtype> is 'article',
'inproceedings' etc. The caret denotes negation, and the tilde denotes
approximate matches instead of exact. For example, '~ceed' would match the
'proceedings', 'inproceedings' and 'mvproceedings' entries. The language for
fields is slightly more involved:

Field occurrence: "[^]<field_name>"
Field values    : "[^]<field_name>(=|~)<value>"
Field range     : "[^]<field_name>(<|>|<=|>=|=)<numeric_value>"
Field range     : "[^]<numeric_value>(<|<=)<field_name>(<|<=)<numeric_value>"
Field range     : "[^]<field_name>=<numeric_value>-<numeric_value>"

All punctuation has the same meaning as for keys and entries. Here are some
example queries:

Find entries that have a publisher field.
>>> bibgrep --field="publisher"

Find entries that do not have a note field.
>>> bibgrep --field="^note"

Find entries where the author is exactly 'D. A. Johnson' and the title contains
the word 'concurrency'.
>>> bibgrep --field="author=D. A. Johnson" --field="title~concurrency"

Find entries that were published in 2001 or later and whose volume is not
between 11 and 50.
>>> bibgrep --field="year>=2001" --field="^10<volume<=50"

Find entries that were published between 2000 and 2018 inclusive.
>>> bibgrep --field="year=2000-2018"

"""

import argparse
import bibpy
import bibpy.parser
import bibpy.tools
import itertools
import operator
import re
import os
import signal
import sys

__author__ = bibpy.__author__
__version__ = '0.1.0'
__license__ = bibpy.__license__

# TODO: How to combine predicates with '&&' and '||'?
# TODO: Make approximate matches use regexes

_DESCRIPTION = """Grep bib(la)tex files satisfying some predicates."""

_NAME_TO_OPERATOR = {
    '<':  operator.lt,
    '>':  operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
    '=':  operator.eq
}


def sigterm_handler(signum, stack_frame):
    """Handle SIGTERM signal."""
    sys.exit('bibgrep: Caught SIGTERM')


# Set up a signal handler for SIGTERM
signal.signal(signal.SIGTERM, sigterm_handler)


class BibgrepError(Exception):
    """Exception class for errors specific to bibgrep."""

    pass


def approx_field_predicate(field, value, args):
    """Return a function that does an approximate match of a string."""
    flags = re.I if args.ignore_case else 0

    def _approx_match(entry):
        field_value = getattr(entry, field, None)

        if field_value is None:
            return False
        else:
            return re.search(value, field_value, flags)

    return _approx_match


def exact_field_predicate(field, value, args):
    """Return a function that does an exact match of a string."""
    func = str.lower if args.ignore_case else str

    def _exact_match(entry):
        return func(getattr(entry, field, '')) == func(value)

    return _exact_match


def field_occurrence_predicate(field, args):
    """Return a function that checks for the occurrence of a field."""
    newfield = field.lower() if args.ignore_case else field

    def _field_occurrence(entry):
        return bool(getattr(entry, newfield, None))

    return _field_occurrence


def negate(func):
    """Return a new function that negates the boolean result of func."""
    def _negate(entry):
        return not func(entry)

    return _negate


def operator_from_string(op_name):
    """Return an operator function from its string equivalent."""
    op = _NAME_TO_OPERATOR.get(op_name, None)

    if op is None:
        raise BibgrepError("Invalid operator '{0}'".format(op_name))

    return op


def comparison_predicate(field, op_name, value):
    """Return a predicate function that compares a field to a value."""
    operator = operator_from_string(op_name)

    def _comparison_predicate(entry):
        if not field:
            return False

        attr = getattr(entry, field, None)

        try:
            return attr and operator(int(attr), int(value))
        except ValueError:
            raise BibgrepError(
                "Cannot compare '{0}' with '{1}'".format(value, attr)
            )

    return _comparison_predicate


def check_and_get_bounds(lower, upper):
    """Convert string bounds to integers and check if lower <= upper."""
    try:
        ilower = int(lower)
        iupper = int(upper)
    except ValueError:
        raise BibgrepError('Bounds cannot be converted to integers')

    if ilower > iupper:
        raise BibgrepError('Lower bound must be <= upper bound')

    return ilower, iupper


def interval_predicate(field, lower, upper):
    """Return a predicate function that checks if a field is in an interval."""
    ilower, iupper = check_and_get_bounds(lower, upper)

    def _interval_predicate(entry):
        if not field:
            return False

        attr = getattr(entry, field, None)

        try:
            return attr and ilower <= int(attr) <= iupper
        except ValueError:
            raise BibgrepError(
                "Cannot compare '{0}' with interval [{1}, {2}]"
                .format(attr, lower, upper)
            )

    return _interval_predicate


def range_predicate(lower, op_name1, field, op_name2, upper):
    """Return a predicate function that checks if a field is in a range.

    Example: '1 <= series < 10'

    """
    ilower, iupper = check_and_get_bounds(lower, upper)
    operator1 = operator_from_string(op_name1)
    operator2 = operator_from_string(op_name2)

    def _range_predicate(entry):
        attr = getattr(entry, field, None)

        try:
            if attr:
                iattr = int(attr)
                return operator1(ilower, iattr) and operator2(iattr, iupper)
        except ValueError:
            raise BibgrepError(
                "Cannot compare '{0}' with range {1} {2} field {3} {4}"
                .format(attr, lower, op_name1, op_name2, upper)
            )

    return _range_predicate


def construct_key_entry_predicate(name, key, tokens, args):
    """Return a key/entry predicate to test if they are of given types."""
    f = None
    prefix_op = tokens[0] if tokens[0] else ''

    if prefix_op and not set(prefix_op).issubset(set('^~')):
        raise BibgrepError("Invalid field operator(s) '{0}'".format(tokens[0]))

    if '~' in prefix_op:
        f = approx_field_predicate(key, tokens[1], args)
    else:
        f = exact_field_predicate(key, tokens[1], args)

    if '^' in prefix_op:
        f = negate(f)

    return f


def construct_field_predicate(name, key, tokens, args):
    """Return a predicate function from the parsed tokens of a query."""
    predicate = None

    if name == 'value':
        if tokens[2] == '=':
            predicate = exact_field_predicate(tokens[1], tokens[-1], args)
        elif tokens[2] == '~':
            predicate = approx_field_predicate(tokens[1], tokens[-1], args)
        else:
            raise BibgrepError(
                "Invalid field operator '{0}'".format(tokens[1])
            )
    elif name == 'occurrence':
        predicate = field_occurrence_predicate(tokens[1], args)
    elif name == 'comparison':
        predicate = comparison_predicate(*tokens[1:])
    elif name == 'interval':
        predicate = interval_predicate(*tokens[1:])
    elif name == 'range':
        predicate = range_predicate(*tokens[1:])
    elif name == 'value':
        predicate = comparison_predicate(*tokens[1:])
    else:
        raise BibgrepError('Invalid field query syntax')

    neg = tokens[0] == '^'

    return negate(predicate) if neg else predicate


def construct_predicates(values, predicate_func, key, pred_combiner, args):
    """Return a list of predicates on entries."""
    # Parse and compose all predicates on values given on the command line
    predicates = []

    for value in values:
        name, tokens = bibpy.parser.parse_query(value, key)
        predicates.append(predicate_func(name, key, tokens, args))

    return bibpy.tools.compose_predicates(predicates, pred_combiner)


def filter_entries(entries, predicates):
    """Filter entries based on predicates on entry type, key and fields."""
    for entry in entries:
        if any(pred(entry) for pred in predicates):
            yield entry


def unique_entries(entries):
    """Remove duplicates from a set of entries."""
    return [k for k, _ in itertools.groupby(entries)]


def process_file(source, unique, predicates):
    """Process a single bibliographic file."""
    entries = bibpy.read_file(source).entries

    if unique:
        entries = unique_entries(entries)

    return filter_entries(entries, predicates)


def main():
    parser = argparse.ArgumentParser(prog='bibgrep', description=_DESCRIPTION)

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=bibpy.tools.format_version(__version__)
    )
    parser.add_argument(
        '-e', '--entry',
        action='append',
        help="Print entries matching an entry type (e.g. '@article')"
    )
    parser.add_argument(
        '-k', '--key',
        action='append',
        dest='keys',
        help='Print entries with exact or similar key. For example, '
             "--key='article1 | article2' prints the entries with keys that "
             'match either'
    )
    parser.add_argument(
        '-f', '--field',
        type=str,
        action='append',
        dest='fields',
        help='Print entries that satisfy a list of field constraints'
    )
    parser.add_argument(
        '-c', '--count',
        action='store_true',
        help='Only a count of selected lines is written to standard output. '
             'If -n is given, prints a grand total'
    )
    parser.add_argument(
        '-i', '--ignore-case',
        action='store_true',
        help='Perform case insensitive matching. By default, bibgrep is case '
             ' sensitive'
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recursively search listed subdirectories'
    )
    parser.add_argument(
        '-u', '--unique',
        action='store_true',
        help='Print only one entry if duplicates are encountered'
    )
    parser.add_argument(
        '-n', '--no-filenames',
        action='store_true',
        help='Do not print filename headers before each entry when --count is '
             'given. Overrides --abbreviate-filenames'
    )
    parser.add_argument(
        '-a', '--abbreviate-filenames',
        action='store_true',
        help='Display only filename and not the full path when --count is '
             ' given'
    )

    args, rest = parser.parse_known_args()

    key_predicate = bibpy.tools.always_false
    entry_predicate = bibpy.tools.always_false
    field_predicate = bibpy.tools.always_false

    try:
        if args.keys:
            key_predicate = construct_predicates(
                args.keys,
                construct_key_entry_predicate,
                'bibkey',
                any,
                args
            )

        if args.entry:
            bibtypes = [
                e for es in args.entry for e in map(str.strip, es.split(','))
            ]
            entry_predicate = construct_predicates(
                bibtypes,
                construct_key_entry_predicate,
                'bibtype',
                any,
                args
            )

        if args.fields:
            field_predicate = construct_predicates(
                args.fields,
                construct_field_predicate,
                'field',
                any,
                args
            )
    except (BibgrepError, bibpy.error.ParseException) as ex:
        sys.exit('{0}'.format(ex))

    if not args.keys and not args.entry and not args.fields:
        # If no constraints are defined, all entries pass
        key_predicate = bibpy.tools.always_true
        entry_predicate = bibpy.tools.always_true
        field_predicate = bibpy.tools.always_true

    filtered_entries = []
    total_count = 0
    predicates = [entry_predicate, key_predicate, field_predicate]

    try:
        if not rest:
            filtered_entries = process_file(sys.stdin, args.unique, predicates)

            if args.count:
                num_entries = len(list(filtered_entries))
                total_count += num_entries
                filtered_entries = []
        else:
            bib_files = bibpy.tools.iter_files(rest, '*.bib', args.recursive)

            for filename in bib_files:
                filtered_entries += list(
                    process_file(filename, args.unique, predicates)
                )

                if args.count:
                    if args.no_filenames:
                        total_count += len(filtered_entries)
                    else:
                        if args.abbreviate_filenames:
                            filename = os.path.basename(filename)

                        print('{0}:{1}'.format(
                            filename, len(filtered_entries))
                        )

                    filtered_entries = []
    except (IOError, bibpy.error.ParseException, BibgrepError) as ex:
        sys.exit('bibgrep: {0}'.format(ex))
    except KeyboardInterrupt:
        sys.exit(1)

    if args.count and (args.no_filenames or not rest):
        print(total_count)

    if filtered_entries:
        # Write all filtered entries to sys.stdout
        print(bibpy.write_string(filtered_entries))

    bibpy.tools.close_output_handles()


if __name__ == "__main__":
    main()
