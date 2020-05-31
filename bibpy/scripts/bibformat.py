#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""bibformat is a command line tool for formatting bibliographic entries."""

import argparse
import bibpy
import bibpy.tools
import collections
import sys

__author__ = bibpy.__author__
__version__ = '0.1.0'
__license__ = bibpy.__license__

_DESCRIPTION = "Format and prettify bibliographic entries. Ignores comments."


def process_file(path, args):
    """Process a single bib file."""
    # Iterate the files given on the command line
    results = bibpy.read_file(path, format='relaxed')

    if args.inherit_crossreferences:
        bibpy.inherit_crossrefs(results.entries)

    if args.inherit_xdata:
        bibpy.inherit_xdata(results.entries)

    if args.expand_string_vars:
        # Expand string variables after crossref and xdata inheritance
        bibpy.expand_strings(results.entries, results.strings)

    if args.order:
        if args.order.lower() == 'true':
            args.order = True
        else:
            args.order = [
                order.strip() for order in
                [e.strip() for e in args.order.split(',')]
            ]

    return results


def main():
    parser = argparse.ArgumentParser(
        prog='bibformat',
        description=_DESCRIPTION
    )

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=bibpy.tools.format_version(__version__)
    )
    parser.add_argument(
        '-c', '--inherit-crossreferences',
        action='store_true',
        help='Inherit all crossreference fields'
    )
    parser.add_argument(
        '-x', '--inherit-xdata',
        action='store_true',
        help='Inherit all xdata fields'
    )
    parser.add_argument(
        '-t', '--expand-string-vars',
        action='store_true',
        help='Expand all string variables'
    )
    parser.add_argument(
        '-a', '--align',
        action='store_true',
        help='Align the equal signs of all fields.'
    )
    parser.add_argument(
        '-i', '--indent',
        type=str,
        default=' ' * 4,
        help='The indentation for all fields.'
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recursively search listed subdirectories'
    )
    parser.add_argument(
        '-s', '--surround',
        type=str,
        default='{}',
        help='The opening and closing characters surrounding field values. '
             'Default is \'{}\''
    )
    parser.add_argument(
        '-o', '--order',
        type=str,
        default=False,
        help='The order in which fields are output. Fields not in this list '
             'are output in an unspecified order after any ordered fields.'
    )
    parser.add_argument(
        '-g', '--group',
        action='store_true',
        help='Group entries alphabetically by type.'
    )

    args, rest = parser.parse_known_args()

    try:
        entries = bibpy.tools.read_files('bibformat', rest, process_file, args)
    except (IOError, bibpy.error.ParseException) as ex:
        sys.exit('bibformat: {0}'.format(ex))
    except KeyboardInterrupt:
        sys.exit(1)

    if args.group:
        groups = collections.defaultdict(list)

        for entry in entries:
            groups[entry.bibtype].append(entry)

        entries = sorted(
            [entry for group in groups for entry in groups[group]],
            key=lambda e: e.bibtype
        )

    format_options = {
        f: getattr(args, f) for f in ['align', 'indent', 'order', 'surround']
    }

    print(bibpy.write_string(entries, **format_options))

    bibpy.tools.close_output_handles()


if __name__ == '__main__':
    main()
