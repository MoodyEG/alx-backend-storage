#!/usr/bin/env python3
""" Our main file """


import redis
import uuid
from typing import Any, Union


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
