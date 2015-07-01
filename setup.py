#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='cegads-domestic-model',
    version='0.3',
    description='An energy consumption model for domestic appliances',
    author='Graeme Stuart',
    author_email='gstuart@dmu.ac.uk',
    url='https://github.com/IESD/cegads-domestic-model',
    packages=find_packages(),
    package_data={'cegads': ['data/*.csv']},
)
