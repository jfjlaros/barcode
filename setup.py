import sys
from setuptools import setup

if sys.version_info < (2, 6):
    raise Exception('barcode requires Python 2.6 or higher.')

# Todo: How does this play with pip freeze requirement files?
requires = ['python-Levenshtein']

# Python 2.6 does not include the argparse module.
try:
    import argparse
except ImportError:
    requires.append('argparse')

import barcode as distmeta

setup(
    name='barcode',
    version=distmeta.__version__,
    description='Design NGS barcodes.',
    long_description=distmeta.__doc__,
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    url=distmeta.__homepage__,
    license='MIT License',
    platforms=['any'],
    packages=['barcode'],
    install_requires=requires,
    entry_points = {
        'console_scripts': [
            'barcode = barcode.cli:main'
        ]
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    keywords='bioinformatics'
)
