from typing import Iterable


def exists(predicate, iterable: Iterable):
    for elem in iterable:
        if predicate(elem):
            return True
    return False

def atmost(n: int, predicate, iterable: Iterable):
    if n < 0:
        return False
    for elem in iterable:
        if predicate(elem):
            if n == 0:
                return False
            n -= 1
    return True
