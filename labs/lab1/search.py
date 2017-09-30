"""CSC148 Lab 1

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains a function that searches for an item in a list,
and illustrates how to use doctest.
"""


def binary_search(lst: list, t: object) -> int:
    """Return the index of <t> in <lst>, or -1 if it does not occur.

    Preconditions:
    - L is sorted.
      Specifically, lst[0] <= lst[1] ... <= lst[n-1], where n is len(lst).
    - t can be compared to the elements of lst.

    >>> binary_search([2, 4, 7, 8, 11], 11)
    4
    >>> binary_search([2, 4, 7, 8, 11], 5)
    -1
    """
    first = 0
    last = len(lst) - 1
    while first < last:
        mid = (last + first) // 2
        if t < lst[mid]:
            last = mid - 1
        else:
            first = mid + 1
    if lst[first] == t:
        return first
    else:
        return -1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
