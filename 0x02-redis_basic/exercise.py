#!/usr/bin/env python3
""" Our main file """


import redis
import uuid
from typing import Any, Union, Callable


class Cache:
    """ Our cache class """

    def __init__(self):
        """ Init the cache """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store the data """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Union[Callable, None] = None) -> Any:
        """ Get the data in the desired format """
        data = self._redis.get(key)
        if not data:
            return None

        if fn:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """ Get the data as a string """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ Get the data as an integer """
        return self.get(key, int)
