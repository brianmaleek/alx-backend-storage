#!/usr/bin/env python3

"""
- Description: Python function that inserts a new document in a collection
                based on kwargs:
- Prototype: def insert_school(mongo_collection, **kwargs):
- mongo_collection will be the pymongo collection object
- Returns: the new _id
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs

    Args:
        mongo_collection: Pymongo collection object
        kwargs: Keyword arg representing the fields and values for the new
        document

    Returns:
    - The new _id of the inserted document
    """
    return mongo_collection.insert_one(kwargs).inserted_id
