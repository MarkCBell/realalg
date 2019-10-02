#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The setup script.'''

from setuptools import setup, find_packages

# We need one of cypari or cypari2 to interface with PARI. Since we do not
# want to lock in the user to either version explicitly, we do not add a
# dependency here but complain at runtime if neither can be found.
requirements = [
    'sympy',
]

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='realalg',
    version='0.1.3',
    description='For manipulating real algebraic numbers',
    long_description=readme(),
    author='Mark Bell',
    author_email='mcbell@illinois.edu',
    url='https://github.com/MarkCBell/realalg',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license='MIT License',
    zip_safe=False,
    keywords='algebraic',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
        ],
)

