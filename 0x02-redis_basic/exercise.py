#!/usr/bin/env python3
""" Our main file """


import redis
import uuid
from functools import wraps
from typing import Any, Union, Callable, List


def replay(method: Callable) -> None:
    """ Display the history of calls of a particular function """
    client = redis.Redis()
    key = method.__qualname__
    inputs = client.lrange("{}:inputs".format(key), 0, -1)
    outputs = client.lrange("{}:outputs".format(key), 0, -1)
    print("{} was called {} times:".format(
        key, client.get(key).decode('utf-8')))
    for inp, outp in zip(inputs, outputs):
        print("{}(*('{}',)) -> {}".format(
            key, inp.decode('utf-8'), outp.decode('utf-8')))


def count_calls(method: Callable) -> Callable:
    """ Count how many times methods of the Cache class are called """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Increment every time the method is called """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Store the history of inputs and outputs """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        in_key = f"{method.__qualname__}:inputs"
        out_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(in_key, *[str(arg) for arg in args])
        output = method(self, *args, **kwargs)
        self._redis.rpush(out_key, str(output))
        return output
    return wrapper


class Cache:
    """ Our cache class """

    def __init__(self):
        """ Init the cache """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
