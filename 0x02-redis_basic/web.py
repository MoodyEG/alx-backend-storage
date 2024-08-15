#!/usr/bin/env python3
""" Get """
import requests
from functools import wraps
from typing import Callable
import redis


client = redis.Redis()


def track_url_access(func: Callable) -> Callable:
    """ Tracker"""
    @wraps(func)
    def wrapper(url: str) -> str:
        """ Decorator for tracker """
        count = "count:" + url
        res = "result:" + url
        client.incr(count)
        cache = client.get(res)
        if cache:
            return cache.decode('utf-8')
        cache = func(url)
        client.set(count, 0)
        client.setex(res, 10, cache)
        return cache
    return wrapper


@track_url_access
def get_page(url: str) -> str:
    """ Get the HTML content of a particular URL """
    response = requests.get(url)
    return response.text
