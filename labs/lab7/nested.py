"""Lab 7: Recursion, Task 2

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few nested list functions for you to practice
implementing recursively.
"""
from typing import Union, List


def nested_max(obj: Union[object, List]) -> int:
    """Return the maximum item stored in nested list <obj>.

    You may assume all the items are positive, and calling
    nested_max on an empty list returns 0.

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    pass


def max_length(obj: Union[object, List]) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    >>> length(17)
    0
    >>> length([1, 2, [1, 2], 4])
    4
    >>> length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    pass


def equal(obj1: Union[object, List], obj2: Union[object, List]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> equal(17, [1, 2, 3])
    False
    >>> equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    pass
