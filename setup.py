#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='wikidata-tree-generator',
    version='0.0.1',
    license=license,
    description="Generating a genealogical tree from a wikidata character",
    long_description=open('README.md').read(),
    author='Louis Mallez',
    packages=find_packages(),
    url='https://github.com/lmallez/wikidata-tree-generator',
    python_requires='>=3.4',
    install_requires=['Wikidata', 'python-gedcom', 'pyyaml']
)
