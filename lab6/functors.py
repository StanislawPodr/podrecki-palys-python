from functools import reduce
from typing import Iterable

#2a
def forall(pred, iterable):
    return all(map(pred, iterable))

#2b
def exists(predicate, iterable: Iterable):
    for elem in iterable:
        if predicate(elem):
            return True
    return False
#2c

def atleast(n, pred, iterable):
    return reduce(lambda acc, x: acc + (1 if pred(x) else 0), iterable, 0) >= n

#2e
def atmost(n: int, predicate, iterable: Iterable):
    if n < 0:
        return False
    for elem in iterable:
        if predicate(elem):
            if n == 0:
                return False
            n -= 1
    return True
