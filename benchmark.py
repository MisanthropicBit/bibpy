"""Run benchmarks on all bib data files."""

import argparse
import bibpy
import fnmatch
import platform
import os
import time
import sys


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
    return "\x1b[{0};1m{1}\x1b[0m".format(color_number, text)


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

    if args.plot:
        sys.exit('--plot option not yet supported')

    if args.color and platform.system().lower().startswith('win'):
        sys.exit('--color option not supported on windows')

    # Filename, # of entries, file size (bytes?), time, status message
    column_format = "{0:<40} {1:<20} {2:<20} {3:<20} {4:<20}"

    print(column_format.format("FILENAME", "ENTRIES", "FILE SIZE", "TIME",
                               "ERRORS?"))

    for filename in iter_files(rest, '*.bib'):
        temp = os.path.basename(filename)
        file_size = os.stat(filename).st_size
        total_time = 0

        for r in range(args.runs):
            try:
                start = time_stamp()
                results = bibpy.read_file(filename, format='relaxed')
                end = time_stamp()

                total_time += end - start
            except bibpy.error.ParseException:
                error = color_string(31, "ERROR") if args.color else "ERROR"
                print(column_format.format(filename, "-", file_size, "-",
                                           error))
                break

            ok = color_string(32, "OK") if args.color else "OK"

            print(column_format.format(temp, len(results.all), file_size,
                                       float(total_time) / float(args.runs),
                                       ok))
