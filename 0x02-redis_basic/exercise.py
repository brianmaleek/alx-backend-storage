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
import json
from typing import Union, Optional, Callable
from functools import wraps


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
    - method: The method to display the history of.

    Returns:
    - None.
    """
    # Create key names for inputs and outputs lists
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    # Get the number of calls to the method
    num_calls = method.__self__._redis.get(method.__qualname__).decode('utf-8')

    # Get the inputs and outputs lists from Redis
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)

    # Print the history of calls
    print("{} was called {} times:".format(method.__qualname__, num_calls))
    for i, (input, output) in enumerate(zip(inputs, outputs)):
        print("{}(*{}) -> {}".format(method.__qualname__,
                                     input.decode('utf-8'),
                                     output.decode('utf-8')))


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function
        in Redis.

    Args:
    - method: The method to be decorated.

    Returns:
    - The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create key names for inputs and outputs lists
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Append the input arguments to the inputs list using RPUSH
        input_data = str(args)  # Convert input arguments to string for storage
        self._redis.rpush(input_key, input_data)

        # Execute the original method to retrieve the output
        output = method(self, *args, **kwargs)

        # Append the output to the outputs list using RPUSH
        output_data = json.dumps(output)  # Convert output to JSON for storage
        self._redis.rpush(output_key, output_data)

        # Return the original output
        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
    - method: The method to be decorated.

    Returns:
    - The decorated method.
    """
    # Use the __qualname__ attribute to get the name of the method
    key = method.__qualname__

    # Create a wrapper function
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorator.

        Args:
        - self: The Redis instance.
        - args: The arguments passed to the method.
        - kwargs: The keyword arguments passed to the method.

        Returns:
        - The result of calling the original method.
        """
        # Increment the number of calls for this particular key
        self._redis.incr(key)

        # Call the original method and return its result
        return method(self, *args, **kwargs)

    # Return the wrapper function
    return wrapper


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

    @call_history
    @count_calls
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

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from Redis using the specified key.

        Args:
        - key: The key associated with the string in Redis.

        Returns:
        - The retrieved string, or None if the key does not exist.
        """
        data = self._redis.get(key)
        return data.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis using the specified key.

        Args:
        - key: The key associated with the integer in Redis.

        Returns:
        - The retrieved integer, or None if the key does not exist.
        """
        data = self._redis.get(key)
        return int(data.decode('utf-8'))
