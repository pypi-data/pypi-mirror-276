from setuptools import setup, find_packages
import os


setup(
    name='PyJONDB',
    version='1.0',
    description='A lightweight, encrypted JSON-based database with support for collections, document operations, and aggregation.',
    long_description=
    """
        # Encrypted JSON Database

        ## Overview
        This package provides a lightweight, encrypted JSON-based database with support for collections, document operations, and aggregation. It uses the `cryptography` library for encryption and decryption of data, ensuring secure storage of your sensitive information.

        ## Features
        - **Encryption and Decryption**: Uses Fernet symmetric encryption to protect your data.
        - **Collections**: Supports creating, reading, updating, and deleting collections.
        - **Documents**: Allows adding, finding, updating, and deleting documents within collections.
        - **Aggregation**: Provides basic aggregation functionality for querying documents.
        - **Linking Collections**: Supports linking between collections to create references.
        - **Tree Structure**: Allows creating tree structures by linking root documents to their child documents.

        ## Usage
        ```python
        import pyjondb

        # Initialize the database
        db = pyjondb.database('mydatabase', 'mysecretkey')

        # Create the database
        db.create()

        # Create a new collection
        db.create_collection('mycollection')

        # Add a document to the collection
        document = {'name': 'John Doe', 'age': 30}
        db.add_document('mycollection', document)

        # Find a document in the collection
        query = {'name': 'John Doe'}
        results = db.find_document('mycollection', query)
        print(results)

        # Update a document in the collection
        document_id = results[0]['_id']
        db.update_document('mycollection', document_id, {'age': 31})

        # Delete a document from the collection
        db.delete_document('mycollection', document_id)

        ### Learn more about it at the docs: https://github.com/t-a-g-o/PyJONDB/wiki
    """,
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
