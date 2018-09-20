from setuptools import setup

import os
import sys

PACKAGE_DIRECTORY = 'lib'

sys.path.append(PACKAGE_DIRECTORY)

import cohesion

requirements_dev_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'requirements-dev.txt')

with open(requirements_dev_filename) as fd:
    tests_require = [i.strip() for i in fd.readlines()]

long_description_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'README.md')

with open(long_description_filename) as fd:
    long_description = fd.read()

setup(
    name=cohesion.__name__,
    version=cohesion.__version__,
    description='A tool for measuring Python class cohesion.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mschwager/cohesion',
    packages=['cohesion'],
    package_dir={'': PACKAGE_DIRECTORY},
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'cohesion = cohesion.__main__:main',
        ],
        'flake8.extension': [
            'H60 = cohesion.flake8_extension:CohesionChecker'
        ],
    },
)
