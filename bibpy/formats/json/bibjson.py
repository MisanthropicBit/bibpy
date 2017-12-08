#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for importing and exporting bib(la)tex to json."""

import json


def _entry_to_json_object(entry, **format_options):
    fields = {field: value for field, value in entry}

    # order = format_options['order']
    # sort_keys = True if order and isinstance(order, bool) else False

    if entry.entry_type in ('comment', 'preamble', 'string'):
        if entry.entry_type == 'string':
            return {entry.entry_type: {entry.variable: entry.value}}
        else:
            return {entry.entry_type: entry.value}
    else:
        return {'entry': {'type':   entry.entry_type,
                          'key':    entry.entry_key,
                          'fields': fields}}

    # indent=indent, sort_keys=sort_keys)


def read_json(string):
    """Read a json string."""
    pass


def read_json_file(source):
    """Read a file containing json."""
    pass


def write_json(entries, **format_options):
    """Export a list of entries to json."""
    # Entry types and keys are not necessarily unique, so we output a list of
    # single entries
    json_entries = [_entry_to_json_object(entry, **format_options)
                    for entry in entries]

    indent = len(format_options['indent'].expandtabs())

    return json.dumps(json_entries, indent=indent)
