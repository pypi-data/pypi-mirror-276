"""
# Utilities

"""
from collections.abc import Iterable, Sized


def chunks(data: Sized, size: int = 1000) -> Iterable:
    """
    Insert list data in chunks as follows:

    >>> for item_ in chunks(['a', 'b', 'c', 'd'], 2): print(item_)
    ['a', 'b']
    ['c', 'd']

    """
    for item in range(0, len(data), size):
        yield data[item:item + size]
