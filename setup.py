#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os.path import join, dirname
from setuptools import setup, find_packages

setup(
    name='core',
    version='1.0',
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

