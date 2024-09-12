"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
from os import path
from typing import Dict

here = path.abspath(path.dirname(__file__))

version: Dict[str, str] = {}
with open(os.path.join(here, 'datemath', '_version.py')) as f:
    exec(f.read(), version)
    VERSION = version['__version__']


setup(
    name='python-datemath',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,
    download_url = 'https://github.com/nickmaccarthy/python-datemath/tarball/{0}'.format(VERSION),

    # The project's main homepage.
    url='https://github.com/nickmaccarthy/python-datemath',


    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    package_data={'': ['*']},
    include_package_data=True,


    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['arrow'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

)
