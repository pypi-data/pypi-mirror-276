#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='my_cool_lib_PG',
    version='0.1.0',
    author='Petr Gregor (SDA)',
    author_email='pe.gregor@gmail.com',
    packages=find_packages(),
    license='GNU GPL',
    include_package_data=True,
    description='Super useful library'
)
