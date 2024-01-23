#!/usr/bin/env python3

"""
- Description: Python function that lists all documents in a collection:
        Prototype: def list_all(mongo_collection):
- Return: an empty list if no document in the collection
- mongo_collection will be the pymongo collection object
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection

    Args:
        mongo_collection: Pymongo collection object

    Returns:
    - A list of documents or an empty list if no document in the collection
    """
    result = []
    document = mongo_collection.find()
    for doc in document:
        result.append(doc)
    return result
