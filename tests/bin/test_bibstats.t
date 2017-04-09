Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibstats --version
    bibstats v0.1.0

Test output

    $ $TESTDIR/../../bin/bibstats $TESTDIR/../data/graphs.bib
    Entry                Count               
    -----------------------------------------
    article              881
    inproceedings        256
    techreport           113
    unpublished          86
    book                 56
    phdthesis            30
    misc                 21
    incollection         7
    mastersthesis        4
    inbook               3
    manual               1
    booklet              1
    
    Total entries: 1459

Test output with percentages

    $ $TESTDIR/../../bin/bibstats --percentages $TESTDIR/../data/graphs.bib
    Entry                Count               
    -----------------------------------------
    article              881 (60.38%)
    inproceedings        256 (17.55%)
    techreport           113 (7.75%)
    unpublished          86 (5.89%)
    book                 56 (3.84%)
    phdthesis            30 (2.06%)
    misc                 21 (1.44%)
    incollection         7 (0.48%)
    mastersthesis        4 (0.27%)
    inbook               3 (0.21%)
    manual               1 (0.07%)
    booklet              1 (0.07%)
    
    Total entries: 1459

Test output with count

    $ $TESTDIR/../../bin/bibstats --count $TESTDIR/../data/small1.bib
    4

Test porcelain output

    $ $TESTDIR/../../bin/bibstats --porcelain $TESTDIR/../data/small1.bib
    article              2
    book                 1
    inproceedings        1

Test --top option

    $ $TESTDIR/../../bin/bibstats --top=3 $TESTDIR/../data/small1.bib
    Entry                Count               
    -----------------------------------------
    article              2
    book                 1
    inproceedings        1
    
    Total entries: 4
