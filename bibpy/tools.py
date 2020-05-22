# -*- coding: utf-8 -*-

"""A collection of functionality for bibpy's accompanying tools."""

import bibpy
import fnmatch
import os
import sys


def format_version(version):
    """Format a version number used by bibpy's accompanying tools."""
    return '%(prog)s v{0}'.format(version)


def always_true(value):
    """A function that always returns True."""
    return True


def always_false(value):
    """A function that always returns False."""
    return False


def compose_predicates(predicates, pred_combiner):
    """Return a function that composes all the given predicates."""
    def composed_predicates(value):
        return pred_combiner(pred(value) for pred in predicates)

    return composed_predicates


def iter_files(names, pattern, recursive):
    """Yield all files matching a specific file pattern in a directory."""
    for name in names:
        if os.path.isdir(name):
            if not recursive:
                sys.exit("'{0}' is a directory, use [-r, --recursive]"
                         " to recurse into directories".format(name))
            else:
                for root, dirs, files in os.walk(name):
                    for filename in fnmatch.filter(files, pattern):
                        yield os.path.join(root, filename)
        else:
            yield name


# NOTE: Function is tested via tests/bin tests
def read_files(program_name, paths, processor, args):  # pragma: no cover
    """Read files from some paths and apply a processor function to each."""
    results = []

    try:
        if not paths:
            # Read from sys.stdin
            results.extend(processor(sys.stdin, args))
        else:
            for filename in iter_files(paths, '*.bib', args.recursive):
                # NOTE: Use scanFile if it ever gets into pyparsing to lazily
                # read and filter the bib source(s)
                results.extend(processor(filename, args))

        return results
    except bibpy.error.ParseException as ex:
        sys.exit("{0}: {1}".format(program_name, ex))
    except KeyboardInterrupt:
        sys.exit(1)


def close_output_handles():
    """Ensure we close stdout and stderr when piping."""
    sys.stdout.close()
    sys.stderr.close()
