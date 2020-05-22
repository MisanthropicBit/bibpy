# -*- coding: utf-8 -*-

"""Test field postprocessing."""

import calendar
import itertools
import random
import sys
import bibpy.date
import bibpy.name
from bibpy.postprocess import postprocess,\
    postprocess_braces,\
    postprocess_namelist,\
    postprocess_keywords,\
    postprocess_int,\
    postprocess_date,\
    postprocess_month,\
    postprocess_keylist,\
    postprocess_pages,\
    postprocess_name,\
    postprocess_functions


def test_postprocess_braces():
    assert postprocess_braces("This is {A} test") == "This is A test"
    assert postprocess_braces("This is {A}     {t}est") == "This is A     test"
    assert postprocess_braces("This is {{  A }}  test") == "This is   A   test"
    assert postprocess_braces("{}This is A test") == "This is A test"
    assert postprocess_braces("This is A test{}") == "This is A test"
    assert postprocess_braces("{T}his is A test") == "This is A test"
    assert postprocess_braces("This is A tes{t}") == "This is A test"

    entry = bibpy.entry.Entry('article', 'key', **{'author': 'Ar{T}hur'})
    postprocess(entry, [], remove_braces=True)
    assert entry.author == 'ArThur'

    entry = bibpy.entry.Entry('article', 'key', **{'author': 'Arthur'})
    postprocess(entry, [], remove_braces=True)
    assert entry.author == 'Arthur'


def test_postprocess_namelist():
    assert postprocess_namelist('author', 'A. B. Cidric and D. E. Fraser') ==\
        ['A. B. Cidric', 'D. E. Fraser']

    assert postprocess_namelist(
        'institution',
        'Department of Communications {and} Data and Department of Computer '
        'Science') == [
            'Department of Communications {and} Data',
            'Department of Computer Science'
        ]

    entry = bibpy.entry.Entry(
        'key',
        'type',
        institution='Department of Communications {and} Data and Department '
                    'of Computer Science',
    )

    postprocess(entry, ['institution'], remove_braces=True)
    assert entry.institution == [
        'Department of Communications and Data',
        'Department of Computer Science'
    ]

    assert postprocess_namelist('institution', '') == []
    assert postprocess_namelist('institution', []) == []

    # Test splitting/parsing names
    assert postprocess_namelist(
        'author', 'A. B. Cidric and D. E. Fraser',
        split_names=['author']
    ) == [
        bibpy.name.Name(first='A. B.', last='Cidric'),
        bibpy.name.Name(first='D. E.', last='Fraser')
    ]

    assert postprocess_namelist(
        'author', 'Hancock, Jeffrey T.',
        split_names=['author']
    ) == [bibpy.name.Name(first='Jeffrey T.', last='Hancock')]

    # Make sure that the 'and' in 'Chandran' is not interpreted as a delimiter
    assert postprocess_namelist(
        'author',
        'L. {Sunil Chandran}',
        split_names=['author']
    ) == [bibpy.name.Name(first='L.', last='Sunil Chandran')]

    assert postprocess_namelist(
        'author',
        'A. B. Cidric and D. E. Fraser',
        split_names=[]
    ) == ['A. B. Cidric', 'D. E. Fraser']


def test_postprocess_names():
    assert postprocess_name('author', 'A. B. Cidric') ==\
        bibpy.name.Name(first='A. B.', last='Cidric')

    assert postprocess_name('author', 'D. E. Fraser') ==\
        bibpy.name.Name(first='D. E.', last='Fraser')

    assert postprocess_name('author', 'Hancock, Jeffrey T.') ==\
        bibpy.name.Name(first='Jeffrey T.', last='Hancock')

    assert postprocess_name('author', 20) == 20
    assert postprocess_name('author', []) == []
    assert postprocess_name('author', '') == ''


def test_postprocess_keywords():
    assert list(postprocess_keywords('key', '')) == []

    assert list(postprocess_keywords('key', 'java;c++; haskell;python')) ==\
        ['java', 'c++', 'haskell', 'python']


def test_postprocess_int():
    assert postprocess_int('month', '2010') == 2010
    assert postprocess_int('month', 'abc') == 'abc'
    assert postprocess_int('doesntmatter', 'abcd') == 'abcd'


def test_postprocess_date():
    d = postprocess_date('date', '1998-05-02')

    assert d.start == bibpy.date.PartialDate(1998, 5, 2)
    assert not d.end
    assert not d.open

    assert postprocess_date('date', '') == bibpy.date.DateRange.empty()


def test_postprocess_month():
    # The first element of calendar.month_name is an empty string
    month_names = list(calendar.month_name)[1:]

    for i, name in enumerate(month_names):
        assert postprocess_month('month', str(i + 1)) == name


def test_postprocess_month_bounds():
    assert postprocess_month('month', 'orsngpi')
    assert postprocess_month('month', 'Jnauary')
    assert postprocess_month('month', 'dec.')


def test_postprocess_month_abbreviations():
    assert postprocess_month('month', 'jan') == 'January'
    assert postprocess_month('month', 'feb') == 'February'
    assert postprocess_month('month', 'mar') == 'March'
    assert postprocess_month('month', 'apr') == 'April'
    assert postprocess_month('month', 'may') == 'May'
    assert postprocess_month('month', 'jun') == 'June'
    assert postprocess_month('month', 'jul') == 'July'
    assert postprocess_month('month', 'aug') == 'August'
    assert postprocess_month('month', 'sep') == 'September'
    assert postprocess_month('month', 'oct') == 'October'
    assert postprocess_month('month', 'nov') == 'November'
    assert postprocess_month('month', 'dec') == 'December'


def generate_invalid_month():
    r = random.randint(-sys.maxsize - 1, sys.maxsize)

    while True:
        while r >= 1 and r <= 12:
            r = random.randint(-sys.maxsize - 1, sys.maxsize)

        yield r


def test_postprocess_month_fail():
    for i in itertools.islice(generate_invalid_month(), 100):
        assert postprocess_month('month', i) == i


def test_postprocess():
    entry = bibpy.read_file('tests/data/preprocess.bib', 'relaxed').entries[0]

    expected = {
        'address':       ['Arthur Cunnings', 'Michelle Toulouse'],
        'afterword':     ['Arthur Cunnings', 'Michelle Toulouse'],
        'annotator':     ['Arthur Cunnings', 'Michelle Toulouse'],
        'author':        ['Arthur Cunnings', 'Michelle Toulouse'],
        'bookauthor':    ['Arthur Cunnings', 'Michelle Toulouse'],
        'commentator':   ['Arthur Cunnings', 'Michelle Toulouse'],
        'date':          bibpy.date.DateRange(
            (1999, 3, 21),
            (None, None, None),
            False
        ),
        'edition':       2,
        'editor':        ['Arthur Cunnings', 'Michelle Toulouse'],
        'editora':       ['Arthur Cunnings', 'Michelle Toulouse'],
        'editorb':       ['Arthur Cunnings', 'Michelle Toulouse'],
        'editorc':       ['Arthur Cunnings', 'Michelle Toulouse'],
        'eventdate':     bibpy.date.DateRange(
            (2008, 12, 7),
            (None, None, None),
            True
        ),
        'foreword':      ['Arthur Cunnings', 'Michelle Toulouse'],
        'holder':        ['Arthur Cunnings', 'Michelle Toulouse'],
        'institution':   ['Arthur Cunnings', 'Michelle Toulouse'],
        'introduction':  ['Arthur Cunnings', 'Michelle Toulouse'],
        'keywords':      ['information', 'data', 'communications'],
        'location':      ['Arthur Cunnings', 'Michelle Toulouse'],
        'language':      ['Arthur Cunnings', 'Michelle Toulouse'],
        'month':         'October',
        'number':        28,
        'organization':  ['Arthur Cunnings', 'Michelle Toulouse'],
        'origlocation':  ['Arthur Cunnings', 'Michelle Toulouse'],
        'origpublisher': ['Arthur Cunnings', 'Michelle Toulouse'],
        'pages':         (11, 20),
        'pagetotal':     205,
        'publisher':     ['Arthur Cunnings', 'Michelle Toulouse'],
        'related':       ['key1', 'key2', 'key3'],
        'school':        ['Arthur Cunnings', 'Michelle Toulouse'],
        'shortauthor':   ['Arthur Cunnings', 'Michelle Toulouse'],
        'shorteditor':   ['Arthur Cunnings', 'Michelle Toulouse'],
        'translator':    ['Arthur Cunnings', 'Michelle Toulouse'],
        'origdate':      bibpy.date.DateRange(
            (2016, 10, 19),
            (None, None, None),
            False
        ),
        'urldate':       bibpy.date.DateRange(
            (2016, 10, 19),
            (2016, 10, 27),
            False
        ),
        'volume':        83,
        'xdata':         ['key1', 'key2', 'key3'],
        'year':          2016,
    }

    # Ensure that there are no duplicates
    assert len(expected.keys()) == len(set(expected.keys()))
    assert len(postprocess_functions.keys()) ==\
        len(set(postprocess_functions.keys()))

    assert set(expected.keys()) == set(postprocess_functions.keys())

    postprocess(entry, expected.keys())

    for field, value in entry:
        assert value == expected.get(field, value)


def test_postprocess_keylist():
    keys = list(postprocess_keylist(
        'key', 'key1,key2, key3, key4 ,      key5,'
    ))

    assert keys == ['key1', 'key2', 'key3', 'key4', 'key5']


def test_postprocess_pages():
    assert postprocess_pages('pages', '1--200') == (1, 200)
    assert postprocess_pages('pages', '1-200') == (1, 200)
    assert postprocess_pages('pages', '1/200') == '1/200'
    assert postprocess_pages('pages', '--200') == '--200'
    assert postprocess_pages('pages', '1--') == '1--'


def test_no_postprocess():
    entry = bibpy.entry.Entry(
        'techreport',
        'ula22',
        **{
            'random_field': 23,
            'nopostprocess': "OK!"
        }
    )

    postprocess(entry, True)
    entry.random_field == 23
    entry.nopostprocess == 'OK!'

    postprocess(entry, ['random_field', 'nopostprocess'])
    entry.random_field == 23
    entry.nopostprocess == 'OK!'
