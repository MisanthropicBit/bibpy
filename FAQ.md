# FAQ

## Q: Why are the key and type properties of entries prefixed with 'bib'? Why not simply name them 'key' and and 'type'?

In bibtex and biblatex, there are already 'key' and a 'type' fields. The 'key'
field is:

> Used for alphabetizing, cross referencing, and creating a label when the
> “author” information (described in Section 4) is missing. - *Bibtex
> documentation*

The 'type' field is:

> The type of a technical report—for example, “Research Note”. - *Bibtex
> documentation*

## Q: Why are there no conversion functions from and to JSON, XML, YAML etc.?

There are already a ton of excellent tools for the job such as
[pandoc](https://pandoc.org/), and I did not want to reinvent the wheel.
Moreover, there are none or few standardised bibliography formats for the other
file formats, making it hard to support.
