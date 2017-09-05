#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for importing and exporting bib(la)tex to bibtexml."""

import xml.dom.minidom
import xml.etree.ElementTree as ET


def _fields_to_xml(xml_entry, entry):
    """Export all the fields of an entry to xml."""
    for field, value in entry:
        xml_field = ET.SubElement(xml_entry, field)
        xml_field.text = str(value)


def to_xml(entries, **format_options):
    """Export a list of entries to xml."""
    root = ET.Element('entries')

    for entry in entries:
        if entry.entry_type in ('comment', 'preamble', 'string'):
            xml_entry = ET.SubElement(root, entry.entry_type)

            if entry.entry_type == 'string':
                xml_field = ET.SubElement(xml_entry, 'variable',
                                          name=entry.variable)
                xml_field.text = entry.value
            else:
                xml_entry.text = entry.value
        else:
            xml_entry = ET.SubElement(root, 'entry',
                                      type=entry.entry_type,
                                      key=entry.entry_key)

            _fields_to_xml(xml_entry, entry)

    reparsed = xml.dom.minidom.parseString(ET.tostring(root, encoding='utf-8'))

    return reparsed.toprettyxml(indent=format_options['indent'],
                                encoding='utf-8').strip()
