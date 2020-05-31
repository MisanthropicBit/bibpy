#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""bibstats is a tool for displaying statistics about bibliographic files.

The default mode displays the count for each entry type in one or more files.
The bibgrep tool can be used to filter out certain entries before passing them
to bibstats, e.g. the following commands pick all entries where 'Adam'
(case-sensitive) appears as an author, then displays the statistics for those
entries:

    $ bibgrep --fields="author~Adam" | bibstats

"""

import argparse
import bibpy
import bibpy.tools
import collections
import sys

__author__ = bibpy.__author__
__version__ = '0.1.0'
__license__ = bibpy.__license__


def process_file(path, args):
    """Process a single bib file."""
    return bibpy.read_file(path).entries


def header(titles, spacing=20, underline='-'):
    """Return a title header as a string."""
    header = ' '.join([
        ('{0:<' + str(spacing) + '}').format(title, spacing)
        for title in titles]
    )

    return header + '\n' + underline * len(header)


def print_stats(stats, print_percentages, total):
    """Print statistics in a column-aligned format."""
    for bibtype, count in stats:
        if print_percentages:
            print('{0:<20} {1} ({2:.2f}%)'.format(
                bibtype,
                count,
                count / float(total) * 100.
            ))
        else:
            print('{0:<20} {1}'.format(bibtype, count))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-v', '--version',
        action='version',
        version=bibpy.tools.format_version(__version__)
    )
    parser.add_argument(
        '-c', '--count',
        action='store_true',
        help='Print only a total count of all entries'
    )
    parser.add_argument(
        '--porcelain',
        action='store_true',
        help='Output results so they are easier to parse by other programs'
    )
    parser.add_argument(
        '-p', '--percentages',
        action='store_true',
        help='Show percentages in addition to counts'
    )
    parser.add_argument(
        '-s', '--sort-entries',
        action='store_true',
        help='Alphabetically sort on entry types instead of number of '
             'occurrences'
    )
    parser.add_argument(
        '-t', '--top',
        type=int,
        default=None,
        help='Display only the top n occurrences.'
    )
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Recursively search listed subdirectories'
    )

    args, rest = parser.parse_known_args()

    try:
        all_entries = bibpy.tools.read_files(
            'bibstats',
            rest,
            process_file,
            args
        )
    except (IOError, bibpy.error.ParseException) as ex:
        sys.exit('bibstats: {0}'.format(ex))
    except KeyboardInterrupt:
        sys.exit(1)

    types = collections.Counter([entry.bibtype for entry in all_entries])
    total = sum(types.values())
    stats = types.most_common(args.top)

    if args.sort_entries:
        stats.sort(key=lambda x: x[0])

    if args.count:
        print(total)
    else:
        if args.porcelain:
            print_stats(stats, args.percentages, total)
        else:
            titles = ['Entry', 'Count']
            print(header(titles))

            print_stats(stats, args.percentages, total)

            print('\nTotal entries: {0}'.format(total))

    bibpy.tools.close_output_handles()


if __name__ == '__main__':
    main()
