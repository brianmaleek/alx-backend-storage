#!/usr/bin/env python3

"""
- Description: Python function returns the list of school having a specific
topic:
- Prototype: def schools_by_topic(mongo_collection, topic):
- mongo_collection will be the pymongo collection object
- topic (string) will be topic searched
"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic

    Args:
        mongo_collection: Pymongo collection object
        topic: Topic searched

    Returns:
    - A list of school having a specific topic
    """
    result = []
    document = mongo_collection.find({"topics": topic})
    for doc in document:
        result.append(doc)
    return result
