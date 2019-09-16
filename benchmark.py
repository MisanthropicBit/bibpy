"""Run benchmarks on all bib data files."""

import argparse
import bibpy
import fnmatch
import platform
import os
import time
import sys


_RED = '31;1'
_GREEN = '32;1'
_LATIN1_ENCODED_FILES = ('cp1252.bib', 'iso-8859-1.bib')


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


def plot(xs, ys):
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
    plt.show()

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='benchmark.py',
                                     description='Benchmark bibpy with '
                                                 'different files')

    parser.add_argument('-p', '--plot', action='store_true',
                        help='Create a barplot of benchmarks')
    parser.add_argument('-r', '--runs', type=int, default=1,
                        help='Run benchmarks this many times and report the '
                             ' average')
    parser.add_argument('-c', '--color', action='store_true',
                        help='Use colors to report results')

    args, rest = parser.parse_known_args()

    if args.color:
        if platform.system().lower().startswith('win'):
            sys.exit('--color option not supported on windows')
        elif args.plot:
            sys.stderr.write('WARNING: --color option does make sense with '
                             '--plot\n')

    # Filename, # of entries, file size (bytes), time, status message
    column_format = '{0:<40} {1:<20} {2:<20} {3:<20} {4:<20}'

    benchmarks = []
    sys.stderr.write('Benchmarking...\n')

    for path in iter_files(rest, '*.bib'):
        filename = os.path.basename(path)
        file_size = os.stat(path).st_size
        total_time = 0

        for r in range(args.runs):
            try:
                encoding = 'utf-8'

                if filename in _LATIN1_ENCODED_FILES:
                    encoding = 'latin1'

                start = time_stamp()
                results = bibpy.read_file(path, format='relaxed',
                                          encoding=encoding)
                end = time_stamp()
                total_time += end - start
            except bibpy.error.ParseException as ex:
                error = color_string(_RED, 'ERROR') if args.color else 'ERROR'

                if not args.plot:
                    benchmarks.append((filename, 0.0, file_size, 0.00, error))

                continue

        ok = color_string(_GREEN, 'OK') if args.color else 'OK'
        benchmarks.append((
            filename,
            len(results.all),
            human_readable_size(file_size),
            '{0:.2f}'.format(float(total_time) / float(args.runs)),
            ok
        ))

    sys.stderr.write('Done...\n')
    benchmarks.sort()

    if args.plot:
        plot([bm[0] for bm in benchmarks], [float(bm[3]) for bm in benchmarks])
    else:
        print(column_format.format('FILENAME', 'ENTRIES', 'FILE SIZE', 'TIME',
                                   'ERRORS?'))

        for path, num_results, file_size, avg_time, status in benchmarks:
            print(column_format.format(path, num_results, file_size, avg_time,
                                       status))
