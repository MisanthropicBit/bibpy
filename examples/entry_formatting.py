"""Example of formatting entries for output in different ways."""

from __future__ import print_function

import bibpy
import os


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


if __name__ == '__main__':
    filename = get_path_for('../tests/data/small1.bib')
    entries = [bibpy.read_file(filename, format='relaxed').entries[0]]

    print("* Default formatting")
    print(bibpy.write_string(entries, align=True, indent='    ', order=[],
                             surround='{}'))

    print()
    print("* Use a tab to indent")
    print(bibpy.write_string(entries, align=True, indent='\t', order=[],
                             surround='{}'))

    print()
    print("* Do not align '=' in entries and enclose field values in double "
          "quotes")
    print(bibpy.write_string(entries, align=False, indent='    ', order=[],
                             surround='""'))

    print()
    print("* Put title, author and year as the first fields (if possible)")
    print(bibpy.write_string(entries, align=True, indent='    ',
                             order=['title', 'author', 'year'],
                             surround='{}'))

    print()
    print("* Order fields alphabetically")
    print(bibpy.write_string(entries, align=True, indent='    ', order=True,
                             surround='{}'))
