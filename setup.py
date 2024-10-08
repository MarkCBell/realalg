#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''The setup script.'''

from setuptools import setup, find_packages

requirements = [
    'numpy>=1.15.1',
    'sympy>=1.6',
]

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='realalg',
    version='0.3.6',
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

