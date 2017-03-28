"""Example of checking the requirements of bibtext and biblatex."""

from __future__ import print_function

import bibpy
import os


def format_requirements_check(required, optional):
    s = ""

    if required:
        s = "required field(s) " + ", ".join(map(str, required))

    if optional:
        if required:
            s += " and "

        temp = ["/".join(map(str, opt)) for opt in optional]
        s += "optional field(s) " + ", ".join(temp)

    return s


def get_path_for(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


if __name__ == '__main__':
    filename = get_path_for('../tests/data/biblatex_missing_requirements.bib')
    entries = bibpy.read_file(filename, format='biblatex').entries

    # Collect all results for which a requirements check failed into a list of
    # pairs. There is also bibpy.requirements.check for checking individual
    # entries
    checked = bibpy.requirements.collect(entries, format='biblatex')

    print("* Using bibpy.requirements.collect:")
    for (entry, (required, optional)) in checked:
        if required or optional:
            # Either a missing required or optional field for this entry
            print("{0}:{1} is missing {2}"
                  .format(entry.entry_type, entry.entry_key,
                          format_requirements_check(required, optional)))

    # Requirements checks can also be performed on individual entries.
    # Use Entry.validate(format) to throw a RequiredFieldError instead of
    # returning a bool
    entry = entries[2]
    print()
    print("* {0} for {1}:{2} = {3}".format("entry.valid('biblatex')",
                                           entry.entry_type,
                                           entry.entry_key,
                                           entry.valid('biblatex')))
