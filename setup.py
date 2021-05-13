#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

packages = find_packages(exclude=('tests',))

requires = [
    'mechanicalsoup'
]

setup_requires = [
    'pytest-runner'
]

tests_require = [
    'pytest'
]

about = {}
with open(os.path.join(here, 'pegass_auth', '__version__.py'), mode='r') as f:
    exec(f.read(), about)

with open('README.md', mode='r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],

    packages=packages,
    install_requires=requires,

    tests_require=tests_require,
    setup_requires=setup_requires,

    author=about['__author__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    license=about['__license__'],
    keywords='pegass croix rouge login authentication',
    project_urls={
        'Bug Reports': 'https://github.com/Annouar/pegass_auth/issues'
    }
)
