"""bibpy module setup script for distribution."""

from __future__ import with_statement

import os
import distutils.core


def get_version(filename):
    with open(filename) as fh:
        for line in fh:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip()[1:-1]


distutils.core.setup(
    name='bibpy',
    version=get_version(os.path.join('bibpy', '__init__.py')),
    author='Alexander Asp Bock',
    author_email='albo.developer@gmail.com',
    platforms='All',
    description=('Bib(la)tex parsing and useful tools'),
    license='MIT',
    keywords='bibpy, bibtex, biblatex, parser',
    url='https://github.com/MisanthropicBit/bibpy',
    packages=['bibpy', 'bibpy.entry', 'bibpy.lexers', 'bibpy.parsers',
              'bibpy.doi'],
    long_description=open('README.md').read(),
    scripts=['bin/bibgrep', 'bin/bibformat', 'bin/bibstats'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6',
    ]
)
