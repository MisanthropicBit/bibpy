Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibgrep --version
    bibgrep v0.1.0

    $ $TESTDIR/../../bin/bibgrep --count $TESTDIR/../data/small1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:4

Test counting

    $ $TESTDIR/../../bin/bibgrep --entry="book" --count $TESTDIR/../data/small1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --entry="book,inproceedings" --count $TESTDIR/../data/small1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:2

    $ $TESTDIR/../../bin/bibgrep --field="issue=3" --count $TESTDIR/../data/small1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --ignore-case --field="journal~logic" --count $TESTDIR/../data/small1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:1

    $ $TESTDIR/../../bin/bibgrep --key="~Co" --count $TESTDIR/../data/small1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:2

    $ $TESTDIR/../../bin/bibgrep --ignore-case --key="~Co" --count $TESTDIR/../data/small1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:2

Test piping

    $ $TESTDIR/../../bin/bibgrep --entry="book" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count
    1

    $ $TESTDIR/../../bin/bibgrep --entry="book,inproceedings" $TESTDIR/../data/small1.bib | $TESTDIR/../../bin/bibgrep --count
    2

Test multiple files

    $ $TESTDIR/../../bin/bibgrep --entry="article" --count $TESTDIR/../data/small1.bib $TESTDIR/../data/simple_1.bib
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/small1.bib:2
    /Users/albo/Dropbox/projects/python/bibpy/tests/bin/../data/simple_1.bib:1
