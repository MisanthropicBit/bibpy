"""Example of name splitting specific fields and filtering entries."""

from __future__ import print_function

import bibpy
import os


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


if __name__ == '__main__':
    # Load just the entries of the file and split names only for 'author'
    # fields
    entries = bibpy.read_file(get_path_for('../tests/data/graphs.bib'),
                              postprocess=True, split_names=True).entries

    # Print the key of each entry that has an author whose last name is
    # 'Fujisawa' (2: KashiwabaraF79 and OhtsukiMKF81)
    for entry in entries:
        if entry.author:
            if any(name.last == 'Fujisawa' for name in entry.author if name):
                print(entry.entry_key)
