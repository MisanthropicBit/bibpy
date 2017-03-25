"""Example of expanding and unexpanding crossreferences."""

from __future__ import print_function

import bibpy
import os


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


def print_entries(entries):
    print(os.linesep.join(map(str, entries)))
    print()


if __name__ == '__main__':
    # Load just the entries of the file
    entries =\
        bibpy.read_file(get_path_for('../tests/data/crossreferences.bib'),
                        format='relaxed').entries

    print("Before inheriting crossreferences")
    print_entries(entries)

    # Inherit crossreferences in-place
    bibpy.inherit_crossrefs(entries, inherit=True, override=False,
                            exceptions={})

    print("After inheriting crossreferences")
    print_entries(entries)

    # Uninherit crossreferences again
    bibpy.uninherit_crossrefs(entries, inherit=True, override=False,
                              exceptions={})

    # The entries should now be the same as before they inherited
    # crossreferences
    print("After uninheriting crossreferences")
    print_entries(entries)
