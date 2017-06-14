from setuptools import setup

import os

requirements_dev_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'requirements-dev.txt')

with open(requirements_dev_filename) as fd:
    tests_require = [i.strip() for i in fd.readlines()]

setup(
    name='cohesion',
    version='0.6.1',
    description='A tool for measuring Python class cohesion.',
    url='https://github.com/mschwager/cohesion',
    packages=['cohesion'],
    package_dir={'': 'lib'},
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'cohesion = cohesion.__main__:main',
        ],
    },
)
