"""Test field postprocessing."""

import bibpy.postprocess
import calendar
import datetime
import itertools
import pytest
import random
import sys


def test_postprocess_namelist():
    assert bibpy.postprocess.postprocess_namelist(
        'A. B. Cidric and D. E. Fraser', name_delimiter='and') ==\
            ['A. B. Cidric', 'D. E. Fraser']

    assert bibpy.postprocess.postprocess_namelist(
        'Department of Communications {and} Data and Department of Computer '
        'Science', name_delimiter='and') ==\
        ['Department of Communications and Data',
         'Department of Computer Science']

    assert bibpy.postprocess.postprocess_namelist('') == []
    assert bibpy.postprocess.postprocess_namelist([]) == []


def test_postprocess_keywords():
    assert list(bibpy.postprocess.postprocess_keywords('')) == []

    assert list(bibpy.postprocess.postprocess_keywords(
        'java;c++; haskell;python', keyword_delimiter=';')) ==\
        ['java', 'c++', 'haskell', 'python']


@pytest.mark.randomize(s=str, str_attrs=('digits',), ncalls=100)
def test_postprocess_int(s):
    assert bibpy.postprocess.postprocess_int('2010') == 2010


def test_postprocess_int_fail():
    assert bibpy.postprocess.postprocess_int('abcd') == 'abcd'


def test_postprocess_date():
    d = bibpy.postprocess.postprocess_date('1998-05-02')

    assert d.start == datetime.date(1998, 5, 2)
    assert d.end is None
    assert not d.open

    assert bibpy.postprocess.postprocess_date('') ==\
        bibpy.date.DateRange(None, None, False)


def test_postprocess_month():
    # The first element of calendar.month_name is an empty string
    month_names = list(calendar.month_name)[1:]

    for i, name in enumerate(month_names):
        assert bibpy.postprocess.postprocess_month(str(i + 1)) == name


def test_postprocess_month_bounds():
    assert bibpy.postprocess.postprocess_month("orsngpi")
    assert bibpy.postprocess.postprocess_month("Jnauary")
    assert bibpy.postprocess.postprocess_month("dec.")


def test_postprocess_month_abbreviations():
    assert bibpy.postprocess.postprocess_month('jan') == 'January'
    assert bibpy.postprocess.postprocess_month('feb') == 'February'
    assert bibpy.postprocess.postprocess_month('mar') == 'March'
    assert bibpy.postprocess.postprocess_month('apr') == 'April'
    assert bibpy.postprocess.postprocess_month('may') == 'May'
    assert bibpy.postprocess.postprocess_month('jun') == 'June'
    assert bibpy.postprocess.postprocess_month('jul') == 'July'
    assert bibpy.postprocess.postprocess_month('aug') == 'August'
    assert bibpy.postprocess.postprocess_month('sep') == 'September'
    assert bibpy.postprocess.postprocess_month('oct') == 'October'
    assert bibpy.postprocess.postprocess_month('nov') == 'November'
    assert bibpy.postprocess.postprocess_month('dec') == 'December'


def generate_invalid_month():
    r = random.randint(-sys.maxsize - 1, sys.maxsize)

    while True:
        while r >= 1 and r <= 12:
            r = random.randint(-sys.maxsize - 1, sys.maxsize)
        yield r


def test_postprocess_month_fail():
    for i in itertools.islice(generate_invalid_month(), 100):
        with pytest.raises(bibpy.error.FieldError):
            assert bibpy.postprocess.postprocess_month(i) == i

    # expected = {
    #     'afterword': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'author': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'bookauthor': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'commentator': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'date': bibpy.date.DateRange(datetime.date(1999, 3, 21), None, False),
    #     'editor': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'editora': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'editorb': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'editorc': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'eventdate': bibpy.date.DateRange(datetime.date(2008, 12, 7), None,
    #                                       True),
    #     'foreword': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'holder': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'institution': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'introduction': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'keywords': ['information', 'data', 'communications'],
    #     'location': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'language': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'month': 'October',
    #     'organization': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'origdate': bibpy.date.DateRange(datetime.date(1630, 2, 1), None,
    #                                      False),
    #     'origlocation': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'origpublisher': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'publisher': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'shortauthor': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'shorteditor': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'translator': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'organization': ['Arthur Cunnings', 'Michelle Toulouse'],
    #     'origdate': bibpy.date.DateRange(datetime.date(2016, 10, 19), None,
    #                                      False),
    #     'urldate': bibpy.date.DateRange(datetime.date(2016, 10, 19),
    #                                     datetime.date(2016, 10, 27),
    #                                     False),
    #     'year': 2016
    # }


def test_postprocess_keylist():
    keys = list(bibpy.postprocess.postprocess_keylist('key1,key2, key3, key4 '
                                                      ',      key5,'))

    assert keys == ['key1', 'key2', 'key3', 'key4', 'key5']


def test_no_postprocess():
    entry = bibpy.entry.Entry('techreport', 'ula22',
                              **{'random_field': 23,
                                 'nopostprocess': "OK!"})

    postprocessed = bibpy.postprocess.postprocess(entry, True)
    assert set(postprocessed) == set([('random_field', 23),
                                      ('nopostprocess', 'OK!')])

    postprocessed = bibpy.postprocess.postprocess(entry, ['random_field',
                                                          'nopostprocess'])
    assert set(postprocessed) == set([('random_field', 23),
                                      ('nopostprocess', 'OK!')])
