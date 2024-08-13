#!/usr/bin/env python3
""" Top students """


def top_students(mongo_collection):
    """ Returns all students sorted by average score """
    students = list(mongo_collection.find())
    for student in students:
        total_score = sum([topic["score"] for topic in student["topics"]])
        student["averageScore"] = total_score / len(student["topics"])
    return sorted(
        students,
        key=lambda student: student["averageScore"],
        reverse=True)
