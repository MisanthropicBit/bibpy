#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Functions for importing and exporting bib(la)tex to bibtexml.

The bibtexml format is described in "BibTEXML: An XML Representation of BibTEX"
by Luca Previtali, Brenno Lurati and Erik Wilde. Currently, the implementation
does no compression using the macro environment, does not split author names
etc. into first and last names, and does not convert LaTeX code into XML
encoded Unicode.

"""

import os
import sys
import xml.dom.minidom
import xml.etree.ElementTree as ET


# TODO: Split up export/import functions?


class BibteXmlError(Exception):
    pass


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


def read_xml(string):
    """Read a bibtexml string."""
    etree = ET.fromstring(string)


def read_xml_file(source):
    """Read a file containing bibtexml."""
    root = ET.parse(source).getroot()

    if root.tag != 'bibliography' or root.attrib:
        raise BibteXmlError("root tag should be '<bibliography>' but was "
                            "'<{0}>'".format(root.tag))

    for child in root:
        if child.tag != 'bibitem':
            raise BibteXmlError("Unknown element '{0}'".format(child.tag))


def _write_line(string, newline=''):
    sys.stdout.write(string + os.path.linesep if not newline else newline)


def _entry_to_bibtexml(entry):
    _write_line('<bibitem type="{0}">'.format(entry.entry_type))
    _write_line('<label>{0}</label>'.format(entry.entry_key))

    for field, value in entry:
        _write_line('<{0}>{1}{2}{1}</{0}>'
                    .format(field, os.path.linesep, value))

    _write_line('</bibitem>')


def write_xml(entries, **format_options):
    """Write a list of entries to bibtexml."""
    _write_line('<bibliography>')

    for entry in entries:
        _entry_to_bibtexml(entry)

    _write_line('</bibliography>')
