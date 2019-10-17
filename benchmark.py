#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Run benchmarks on all bib data files."""

import argparse
import bibpy
from bibpy.error import LexerException, ParseException
import fnmatch
import platform
import os
import time
import sys


_RED = '31;1'
_GREEN = '32;1'
_LATIN1_ENCODED_FILES = ('cp1252.bib', 'iso-8859-1.bib')


class Benchmark(object):
    """Class for holding benchmark data."""

    def __init__(self, filename, byte_size):
        """Create benchmark for a file with a given size."""
        self.filename = filename
        self.byte_size = byte_size
        self.num_entries = 0
        self.data = []
        self.status = ''

    def average(self):
        """Return the average runtime for the benchmark."""
        return sum(self.data) / len(self.data)

    def __lt__(self, other):
        """Sort benchmarks per filename."""
        if not isinstance(other, Benchmark):
            return False

        return self.filename < other.filename


def time_stamp():
    """Attempt to return a portable, precise timer."""
    if sys.version_info >= (3, 3):
        return time.perf_counter()

    return time.clock()


def iter_files(names, pattern):
    """Yield all files matching a specific file pattern in a directory."""
    for name in names:
        if os.path.isdir(name):
            for root, dirs, files in os.walk(name):
                for filename in fnmatch.filter(files, pattern):
                    yield os.path.join(root, filename)
        else:
            yield name


def color_string(color_number, text):
    """Return the text with color codes for the given color."""
    return '\x1b[{0}m{1}\x1b[0m'.format(color_number, text)


def human_readable_size(byte_size):
    """Convert a number of bytes to a human-readable string."""
    i = 0
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

    while byte_size >= 1024 and i < len(suffixes) - 1:
        byte_size /= 1024.
        i += 1

    size = ('{0:.2f}'.format(byte_size)).rstrip('0').rstrip('.')

    return '{0} {1}'.format(size, suffixes[i])


def barplot(xs, ys):
    """Plot data as a barplot with rotated labels."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print('Package matplotlib is not installed and required for plotting')
        return False

    xpos = range(len(xs))
    plt.bar(xpos, ys)
    plt.xlabel('Reference files')
    plt.ylabel('Time (seconds)')
    plt.xticks(xpos, xs, rotation=90)
    plt.subplots_adjust(top=0.95, bottom=0.6)
    plt.ylim(0.0, max(ys) * 1.3)

    for index, value in enumerate(ys):
        fmt = '{0:.4f}' if value < 0.01 else '{0:.2f}'

        plt.text(index, value + 0.05, fmt.format(value),
                 ha='center', rotation=90)

    plt.show()

    return True


def benchmark_file(path, args):
    """Benchmark a single file."""
    filename = os.path.basename(path)
    byte_size = os.stat(path).st_size
    benchmark = Benchmark(filename, human_readable_size(byte_size))

    try:
        for r in range(args.runs):
            encoding = 'utf-8'

            if filename in _LATIN1_ENCODED_FILES:
                encoding = 'latin1'

            start = time_stamp()
            result = bibpy.read_file(path, format='relaxed', encoding=encoding,
                                     postprocess=args.postprocess)
            end = time_stamp()

            benchmark.num_entries = sum([len(r) for r in result])
            benchmark.data.append(end - start)
    except (LexerException, ParseException) as ex:
        error = color_string(_RED, 'ERROR') if args.color else 'ERROR'
        error += ' ({0})'.format(ex)
        benchmark.data.append(0.)
        benchmark.status = error

        return benchmark, False
    else:
        ok = color_string(_GREEN, 'OK') if args.color else 'OK'
        benchmark.status = ok

    return benchmark, True


def parse_args():
    """Parse commandline arguments."""
    parser = argparse.ArgumentParser(prog='benchmark.py',
                                     description='Benchmark bibpy with '
                                                 'different files')

    parser.add_argument('-p', '--plot', action='store_true',
                        help='Create a barplot of benchmarks. Automatically '
                             'skips any files that result in an error')
    parser.add_argument('-r', '--runs', type=int, default=1,
                        help='Run benchmarks this many times and report the '
                             ' average')
    parser.add_argument('-c', '--color', action='store_true',
                        help='Use colors to report results')
    parser.add_argument('-s', '--skip-errors', action='store_true',
                        help='Skip files that result in errors')
    parser.add_argument('-o', '--postprocess', action='store_true',
                        help='Enable entry postprocessing')

    args, rest = parser.parse_known_args()

    if args.color:
        if platform.system().lower().startswith('win'):
            sys.exit('--color option not supported on windows')
        elif args.plot:
            sys.stderr.write('WARNING: --color option does make sense with '
                             '--plot\n')

    if args.skip_errors and args.plot:
        sys.stderr.write('WARNING: Errors automatically skipped when '
                         'plotting\n')

    return args, rest


if __name__ == '__main__':
    args, rest = parse_args()

    # Filename, # of entries, file size (bytes), time, status message
    column_format = '{0:<40} {1:<20} {2:<20} {3:<30} {4:<20}'

    benchmarks = []
    sys.stderr.write('Benchmarking...\n')

    for path in iter_files(rest, '*.bib'):
        benchmark, ok = benchmark_file(path, args)

        if not ok and (args.skip_errors or args.plot):
            continue

        benchmarks.append(benchmark)

    sys.stderr.write('Done...\n')
    benchmarks.sort()

    if args.plot:
        averages = [bm.average() for bm in benchmarks]
        barplot([bm.filename for bm in benchmarks], averages)
    else:
        print(column_format.format('FILENAME', 'ENTRIES', 'FILE SIZE', 'TIME',
                                   'ERRORS?'))

        for bm in benchmarks:
            print(column_format.format(
                        bm.filename,
                        bm.num_entries,
                        bm.byte_size,
                        bm.average(),
                        bm.status
                    ))
