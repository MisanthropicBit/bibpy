Set up PYTHONPATH

    $ PYTHONPATH="$TESTDIR/../.." && export PYTHONPATH

Test version number

    $ $TESTDIR/../../bin/bibformat --version
    bibformat v0.1.0

Verify json output

    $ echo $($TESTDIR/../../bin/bibformat --export=json $TESTDIR/../data/small1.bib) | python -m json.tool > /dev/null

Verify xml output

    $ echo $($TESTDIR/../../bin/bibformat --export=xml $TESTDIR/../data/small1.bib) | python -m xml.dom.minidom > /dev/null
