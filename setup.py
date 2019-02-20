#!/usr/bin/env python
import os
from setuptools import find_packages, setup

setup(
    name='nlp4airbus',
    version='0.2',

    description='My Python library project',

    author='Airbus',

    packages=find_packages(exclude=['contrib', 'docs', 'test']),

    package_data={'nlp4airbus': ['data/*.csv.gz']},

    # Please instead specify your dependencies in conda_recipe/meta.yml
    install_requires=[],
)