"""All valid bib(la)tex fields.

Bibtex (08/02/1988)
Biblatex version 3.2 (27/12/2015)

NOTE: We deviate from PEP8 by specifying global variables as lowercase for
readable access.

"""

__all__ = ('all', 'bibtex', 'biblatex')

# Fields common to both bibtex and biblatex
base_fields = frozenset(
    ['author',
     'booktitle',
     'edition',
     'editor',
     'howpublished',
     'institution',
     'month',
     'note',
     'number',
     'organization',
     'pages',
     'publisher',
     'series',
     'title',
     'type',
     'volume',
     'year']
)

##################################################################
# Bibtex
##################################################################
bibtex_fields = frozenset(
    ['address',
     'annote',
     'chapter',
     'crossref',
     'journal',
     'key',
     'school']
)

bibtex = base_fields | bibtex_fields

##################################################################
# Biblatex
##################################################################
biblatex_fields = frozenset(
    ['abstract',
     'addendum',
     'afterword',
     'annotation',
     'annotator',
     'authortype',
     'bookauthor',
     'bookpagination',
     'booksubtitle',
     'booktitleaddon',
     'chapter',
     'commentator',
     'date',
     'doi',
     'editora',
     'editorb',
     'editorc',
     'editortype',
     'eid',
     'entrysubtype',
     'eprint',
     'eprintclass',
     'eprinttype',
     'eventdate',
     'eventtitle',
     'eventtitleaddon',
     'file',
     'foreword',
     'holder',
     'indextitle',
     'introduction',
     'isan',
     'isbn',
     'isnm',
     'isrn',
     'issn',
     'issue',
     'issuesubtitle',
     'issuetitle',
     'iswc',
     'journalsubtitle',
     'journaltitle',
     'label',
     'language',
     'library',
     'location',
     'mainsubtitle',
     'maintitle',
     'maintitleaddon',
     'nameaddon',
     'origdate',
     'origlanguage',
     'origlocation',
     'origpublisher',
     'origtitle',
     'pagetotal',
     'pagination',
     'part',
     'pubstate',
     'reprinttitle',
     'shortauthor',
     'shorteditor',
     'shorthand',
     'shorthandintro',
     'shortjournal',
     'shortseries',
     'shorttitle',
     'subtitle',
     'titleaddon',
     'translator',
     'url',
     'urldate',
     'venue',
     'version',
     'volumes']
)

##################################################################
# Biblatex special fields
##################################################################
biblatex_special_fields = frozenset(
    ['crossref',
     'entryset',
     'execute',
     'gender',
     'langid',
     'langidopts',
     'ids',
     'indexsorttitle',
     'keywords',
     'options',
     'presort',
     'related',
     'relatedoptions',
     'relatedtype',
     'relatedstring',
     'sortkey',
     'sortname',
     'sortshorthand',
     'sorttitle',
     'sortyear',
     'xdata',
     'xref']
)

biblatex = base_fields | biblatex_fields | biblatex_special_fields

# A list of all the fields of Bib(la)tex
all = biblatex | bibtex
