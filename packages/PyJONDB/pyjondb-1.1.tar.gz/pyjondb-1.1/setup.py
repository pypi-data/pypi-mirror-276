from setuptools import setup, find_packages
import os

desc = open('./database-viewer/pypi.readme').read()

setup(
    name='PyJONDB',
    version='1.1',
    description='A lightweight, encrypted JSON-based database with support for collections, document operations, and aggregation.',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='t-a-g-o',
    author_email='santiago@tago.works',
    url='https://github.com/t-a-g-o/PyJONDB',
    packages=find_packages(),
    install_requires=[
        'cryptography',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
    keywords=[
        'encryption database',
        'encrypted database',
        'json database',
        'secure storage',
        'lightweight database',
        'document store',
        'fernet encryption',
        'cryptography',
        'data security',
        'data encryption',
        'collections',
        'document operations',
        'aggregation',
        'query',
        'NoSQL',
        'python database',
        'uuid',
        'file-based database',
        'local database',
        'secure json',
        'nested data',
        'tree structure',
        'data management',
        'data linkage',
        'collection linking'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/t-a-g-o/PyJONDB/issues',
        'Source': 'https://github.com/t-a-g-o/PyJONDB/',
    },
)
