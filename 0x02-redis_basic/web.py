#!/usr/bin/env python3
""" Get """
import requests
from functools import wraps
from typing import Callable
import redis


def track_url_access(func: Callable) -> Callable:
    """ Tracker"""
    @wraps(func)
    def wrapper(url: str) -> str:
        """ Decorator for tracker """
        key = "count:" + url
        client = redis.Redis()
        client.incr(key)
        cache = client.get(url)
        if cache:
            return cache.decode('utf-8')
        page = func(url)
        client.set(url, page, 10)
        return page
    return wrapper

@track_url_access
def get_page(url: str) -> str:
    """ Get the HTML content of a particular URL """
    response = requests.get(url)
    return response.text
