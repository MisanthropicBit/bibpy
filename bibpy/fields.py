"""All valid bib(la)tex fields.

Bibtex (08/02/1988)
Biblatex version 3.2 (27/12/2015)

NOTE: We deviate from PEP8 by specifying global variables as lowercase for
readable access.

"""

# Ignore E501: line too long errors
# flake8: noqa

__all__ = ('all', 'bibtex', 'biblatex')

# Fields common to both bibtex and biblatex
base_fields_docs = {
    'author':       'The author(s) of the work',
    'booktitle':    'The title of a larger publication which this work is '
                    'part of',
    'edition':      'The edition of a printed publication',
    'editor':       'The editor(s) of the title, booktitle, or maintitle, '
                    'depending on the entry',
    'howpublished': 'A notice for unusual publications which do not fit into '
                    'any of the common categories',
    'institution':  'The name of a university or some other institution',
    'month':        'An annex to the maintitle',
    'note':         'Miscellaneous bibliographic data which does not fit into '
                    'any other field',
    'number':       """The number of a journal or the volume/number of a book in a series.

With @patent entries, this is the number or record token of a patent or patent
request. Normally this field will be an integer or an integer range, but it may
also be a short designator that is not entirely numeric such as 'S1',
'Suppl. 2', '3es'.

""",
    'organization': 'The organization(s) that published a @manual or @online '
                    'resource, or sponsored a conference',
    'pages':        'One or more page numbers or page ranges',
    'publisher':    'The name(s) of the publisher(s)',
    'series':       """The name of a publication series.

E.g. 'Studies in ...', or the number of a journal series. Books in a
publication series are usually numbered. The number or volume of a book in
a series is given in the number field

""",
    'title':        'The title of the work',
    'type':         'The type of a manual, patent, report, or thesis',
    'volume':       'The volume of a multi-volume book or a periodical',
    'year':         'The year of publication',
}

base_fields = frozenset(base_fields_docs)

##################################################################
# Bibtex (these fields also appear as aliases for backwards
# compatibility in Biblatex)
##################################################################
bibtex_fields_docs = {
    'address':      'An alias for location, provided for BibTeX compatibility',
    'annote':       'An alias for annotation, provided for jurabib '
                    'compatibility',
    'chapter':      'A chapter or section or any other unit of a work',
    'crossref':     'An entry key for cross-referencing',
    'journal':      'An alias for journaltitle, provided for BibTeX '
                    'compatibility',
    'key':          'An alias for sortkey, provided for BibTeX compatibility',
    'pdf':          'An alias for file, provided for JabRef compatibility',
    'primaryclass': 'An alias for eprintclass, provided for arXiv '
                    'compatibility',
    'school':       'An alias for institution, provided for BibTeX '
                    'compatibility',
}

bibtex = base_fields | frozenset(bibtex_fields_docs)

##################################################################
# Biblatex
##################################################################
biblatex_fields_docs = {
    'abstract':        'Abstract of the bibliography entry',
    'addendum':        'Miscellaneous bibliographic data',
    'afterword':       'The author(s) of an afterword to the work',
    'annotation':      """Annotation for annotated bibliographies.

Not related to the annotator field.

""",
    'annotator':       'The author(s) of annotations to the work',
    'authortype':      'The type of author',
    'bookauthor':      'The author(s) of the booktitle',
    'bookpagination':  'If the work is published as part of another, this is '
                       'the pagination scheme of the enclosing work',
    'booksubtitle':    'The subtitle related to the booktitle',
    'booktitleaddon':  'An annex to the booktitle',
    'chapter':         bibtex_fields_docs['chapter'],
    'commentator':     'The author(s) of a commentary to the work',
    'date':            'The publication date',
    'doi':             'The Digital Object Identifier of the work',
    'editora':         'A secondary editor performing a different editorial '
                       'role, such as compiling, redacting, etc.',
    'editorb':         'Another secondary editor performing a different role',
    'editorc':         'Another secondary editor performing a different role',
    'editortype':      'The type of editorial role performed by the editor',
    'editoratype':     'Similar to editortype but referring to the editora '
                       'field',
    'editorbtype':     'Similar to editortype but referring to the editorb '
                       'field',
    'editorctype':     'Similar to editortype but referring to the editorc '
                       'field ',
    'eid':             'The electronic identifier of an @article',
    'entrysubtype':    'The subtype of an entry type',
    'eprint':          'The electronic identifier of an online publication',
    'eprintclass':     """Additional information related to the resource indicated by the eprinttype field.

    This could be a section of an archive, a path indicating a service, a
    classification of some sort, etc.

""",
    'eprinttype':      """The type of eprint identifier.

E.g. the name of the archive, repository, service, or system the eprint
field refers to.

""",
    'eventdate':       'The date of a conference, a symposium, or some other '
                       'event in @proceedings and @inproceedings entries',
    'eventtitle':      'The title of a conference, a symposium, or some other '
                       'event in @proceedings and @inproceedings entries',
    'eventtitleaddon': """An annex to the eventtitle field.

Can be used for known event acronyms, for example.

""",
    'file':            'A local link to a pdf or other version of the work',
    'foreword':        'The author(s) of a foreword to the work',
    'holder':          'The holder(s) of a @patent, if different from the '
                       'author',
    'indextitle':      'A title to use for indexing instead of the regular '
                       'title',
    'introduction':    'The author(s) of an introduction to the work',
    'isan':            'The International Standard Audiovisual Number of an '
                       'audiovisual work',
    'isbn':            'The International Standard Book Number of a book',
    'isnm':            'The International Standard Music Number for printed '
                       'music such as musical scores',
    'isrn':            'The International Standard Technical Report Number of '
                       'a technical report',
    'issn':            'The International Standard Serial Number of a '
                       'periodical',
    'issue':           """The issue of a journal.

This field is intended for journals whose individual issues are identified
by a designation such as 'Spring' or 'Summer' rather than the month or a
number. Integer ranges and short designators are better written to the
number field.

""",
    'issuesubtitle':   'The subtitle of a specific issue of a journal or '
                       'other periodical',
    'issuetitle':      'The title of a specific issue of a journal or other '
                       'periodical',
    'iswc':            'The International Standard Work Code of a musical '
                       'work',
    'journalsubtitle': 'The subtitle of a journal, a newspaper, or some other '
                       'periodical',
    'journaltitle':    'The name of a journal, a newspaper, or some other '
                       'periodical',
    'label':           """A label to be used by the citation style.

A designation to be used by the citation style as a substitute for the
regular label if any data required to generate the regular label is
missing. For example, when an author-year citation style is generating a
citation for an entry which is missing the author or the year, it may fall
back to label.

""",
    'language':        'The language(s) of the work',
    'library':         'Information such as a library name and a call number.',
    'location':        'The place(s) of publication, i.e., the location of '
                       'the publisher or institution',
    'mainsubtitle':    'The subtitle related to the maintitle',
    'maintitle':       """The main title of a multi-volume book.

E.g. 'Collected Works'.

""",
    'maintitleaddon':  'An annex to the maintitle',
    'nameaddon':       'An addon printed immediately after the author name',
    'origdate':        'The publication date of the original edition if the '
                       'work is a translation, reprint etc.',
    'origlanguage':    'The language(s) of the original work if translated',
    'origlocation':    'The location of the original edition if translated or '
                       'a reprint etc.',
    'origpublisher':   'The publisher of the original edition, if translated '
                       'or a reprint etc.',
    'origtitle':       'The title of the original work if translated',
    'pagetotal':       'The total number of pages of the work',
    'pagination':      'The pagination of the work',
    'part':            'The number of a partial volume',
    'pubstate':        'The name(s) of the publisher(s)',
    'reprinttitle':    'The title of a reprint of the work',
    'shortauthor':     'The author(s) of the work, given in an abbreviated '
                       'form',
    'shorteditor':     'The editor(s) of the work, given in an abbreviated '
                       'form',
    'shorthand':       'A special designation to be used by the citation '
                       'style instead of the usual label',
    'shorthandintro':  '',
    'shortjournal':    'A short version or an acronym of the journaltitle',
    'shortseries':     'A short version or an acronym of the series field',
    'shorttitle':      'The title in an abridged form',
    'subtitle':        'The subtitle of the work',
    'titleaddon':      'An annex to the title',
    'translator':      'The translator(s) of the title or booktitle',
    'url':             'The url of an online publication',
    'urldate':         'The access date of the address specified in the url '
                       'field',
    'venue':           'The location of a conference, a symposium etc. in '
                       '@proceedings and @inproceedings entries',
    'version':         'The revision number of a piece of software, a manual '
                       'etc.',
    'volumes':         'The total number of volumes of a multi-volume work',
}

##################################################################
# Biblatex special fields
##################################################################
biblatex_special_fields = {
    'crossref':       bibtex_fields_docs['crossref'],
    'entryset':       'A field is specific to entry sets',
    'execute':        'A special field which holds arbitrary TeX code',
    'gender':         'The gender of the author or the gender of the editor, '
                      'if there is no author',
    'langid':         'The language id of the bibliography entry',
    'langidopts':     'For polyglossia users, allows per-entry language '
                      'specific options',
    'ids':            'Citation key aliases for the main citation key',
    'indexsorttitle': 'The title used when sorting the index',
    'keywords':       'A separated list of keywords',
    'options':        """A separated list of entry options in <key>=<value> notation.

This field is used to set options on a per-entry basis.

""",
    'presort':        'A special field used to modify the sorting order',
    'related':        'Citation keys of other entries which have a '
                      'relationship to this entry',
    'relatedoptions': 'Per-type options to set for a related entry',
    'relatedtype':    'An identifier which specifies the type of relationship '
                      'for the keys listed in the related field',
    'relatedstring':  'A field used to override the bibliography string '
                      'specified by relatedtype',
    'sortkey':        'A field used to modify the sorting order',
    'sortname':       'A name or a list of names used to modify the sorting '
                      'order',
    'sortshorthand':  'Similar to sortkey but used in the list of shorthands',
    'sorttitle':      'A field used to modify the sorting order',
    'sortyear':       'A field used to modify the sorting order',
    'xdata':          'This field inherits data @xdata entries',
    'xref':           'An alternative cross-referencing mechanism',
}

biblatex = base_fields\
    | frozenset(biblatex_fields_docs)\
    | frozenset(biblatex_special_fields)

# A mapping of all the field docstrings
docstrings = {
    **base_fields_docs,
    **bibtex_fields_docs,
    **biblatex_fields_docs,
    **biblatex_special_fields,
}

# A list of all the fields of Bib(la)tex
all = biblatex | bibtex
