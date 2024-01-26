#!/usr/bin/env python3
"""
- Description: In this tasks, we'll implement a get_page function
    (prototype: def get_page(url: str) -> str:). The core of the function is
    very simple. It uses the requests module to obtain the HTML content of a
    particular URL and returns it.

- Inside get_page track how many times a particular URL was accessed in the
key "count:{url}" and cache the result with an expiration time of 10 seconds.

- Tip: Use http://slowwly.robertomurray.co.uk to simulate a slow response and
test your caching.

Bonus: implement this use case with decorators.
"""

import redis
import requests
from functools import wraps


# Initialize Redis client
redis_client = redis.Redis()


def url_access_count(method):
    """
    Decorator for the get_page function to cache content and track access
    count.

    Args:
    - method: The method to be decorated.

    Returns:
    - The decorated method.
    """
    @wraps(method)
    def wrapper(url):
        """
        Wrapper function that handles caching and access count tracking.

        Args:
        - url: The URL of the page.

        Returns:
        - The HTML content of the page.
        """
        cache_key = f"cached:{url}"
        count_key = f"count:{url}"

        cached_value = redis_client.get(cache_key)

        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        html_content = method(url)

        redis_client.incr(count_key)
        redis_client.setex(cache_key, 10, html_content)

        return html_content

    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.

    Args:
    - url: The URL of the page.

    Returns:
    - The HTML content of the page.
    """
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    # Example usage
    url_to_fetch = 'http://slowwly.robertomurray.co.uk'
    html_content = get_page(url_to_fetch)
    print(f"HTML Content:\n{html_content}")
