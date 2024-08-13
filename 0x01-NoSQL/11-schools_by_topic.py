#!/usr/bin/env python3
""" Search """


def schools_by_topic(mongo_collection, topic):
    """ Search """
    results = mongo_collection.find({"topics": topic})
    return results
