# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use Python Boilerplate to start
# simple, usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os

from setuptools import setup, find_packages

# Meta information
version = open('scripts/VERSION').read().strip()
name    = open('scripts/NAME').read().strip()
author  = 'martyn pratt'
author_email = 'martynjamespratt@gmail.com'
description  = open('scripts/DESCRIPTION').read().strip()
dirname = os.path.dirname(__file__)

# Save version and author to __meta__.py
path = os.path.join(dirname, '__meta__.py')
data = '''# Automatically created. Please do not edit.
__version__ = u'%s'
__author__ = u'F\\xemartyn\\xepratt'
''' % version
with open(path, 'wb') as F:
    F.write(data.encode())
    
setup(
    # Basic info
    name=name,
    version=version,
    author=author,
    author_email=author_email,
    url='https://github.com/martyni/' + name,
    description=description,
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },

    # Data files
    package_data={
        'python_boilerplate': [
            'templates/*.*'
        ],
    },

    # Scripts
    entry_points={
        'console_scripts': [
            name + ' = my_app.app:main'],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
