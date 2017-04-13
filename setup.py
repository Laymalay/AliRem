#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os.path import join, dirname
from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name='core',
    version='1.0',
    install_requires=install_requirements,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    test_suite='my_tests.test_remove',

    entry_points={
        'console_scripts':
            ['alirm = alirem.main:remove',
             'alirs = alirem.main:restore',
             'cleanbasket = alirem.main:clean_basket',
             'showconfig = alirem.main:show_config',
             'showbasket = alirem.main:show_basket_list']
        }

)

