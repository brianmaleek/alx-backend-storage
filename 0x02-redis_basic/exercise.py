#!/usr/bin/env python3

"""
- Create a Cache class. In the __init__ method.
- Store an instance of the Redis client as a private variable named _redis
    (using redis.Redis()) and flush the instance using flushdb.
- Create a store method that takes a data argument and returns a string.
- The method should generate a random key (e.g. using uuid), store the input
    data in Redis using the random key and return the key.
- Type-annotate store correctly. Remember that data can be a str, bytes, int
    or float.
"""

import redis
import uuid
import sys
from typing import Union, Optional, Callable


class Cache:
    """ Cache class
    """
    def __init__(self):
        """
        Initialize the Cache instance with a Redis client and flush the
        Redis database.
        """
        # Create a Redis client instance
        self._redis = redis.Redis()

        # Flush the Redis instance
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis with a random key and return the key.

        Args:
        - data: Input data to be stored. Can be str, bytes, int, or float.

        Returns:
        - A randomly generated key (UUID) used for storing the data in Redis.
        """
        # Generate a random key
        random_key = str(uuid.uuid4())

        # Store the data in Redis using the random key
        self._redis.set(random_key, data)

        # Return the generated random key
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Union[str, bytes, int, float]:
        """
        Get the data stored at the input key and return it.

        Args:
        - key: Key to access the data in Redis.
        - fn: Optional callable function to convert the retrieved data.

        Returns:
        - The data stored at the input key.
        """
        # Get the data stored at the input key
        data = self._redis.get(key)

        # If the function argument is not None, call the function on the data
        if data is not None and fn is not None:
            data = fn(data)

        # Return the data
        return data

    def get_str(self, data: bytes) -> str:
        """
        Retrieve a string from Redis using the specified key.

        Args:
        - key: The key associated with the string in Redis.

        Returns:
        - The retrieved string, or None if the key does not exist.
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """
        Retrieve an integer from Redis using the specified key.

        Args:
        - key: The key associated with the integer in Redis.

        Returns:
        - The retrieved integer, or None if the key does not exist.
        """
        return int.from_bytes(data, sys.byteorder)
