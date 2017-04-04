from os.path import join, dirname
from setuptools import setup, find_packages


setup(
    name='core',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    test_suite='my_tests.test',

    entry_points={
        'console_scripts':
            ['alirem = alirem.main:alirem']
        }

)

