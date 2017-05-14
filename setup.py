#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='boto3_session_cache',
    version='1.0.0',
    packages=[ 'boto3_session_cache' ],
    install_requires=[ 'boto3' ],
    extras_require={
        "test": [ 'pytest>=3.0', 'pyfakefs>=3.1']
    },
    provides=[ 'boto3_session_cache' ],
    author='Justin Menga',
    author_email='justin.menga@gmail.com',
    url='https://github.com/mixja/boto3-session-cache',
    description='Provides a local file system cache for temporary AWS session credentials.',
    keywords='aws sts boto3 credentials',
    license='ISC',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
)