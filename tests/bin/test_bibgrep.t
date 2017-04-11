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
