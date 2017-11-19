"""Lab 9: Binary Search Trees

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains some code for running some timing experiments on
binary search trees.

You'll want to review the documentation of the timer.py module for this part.
"""
import random
import sys

from bst import BinarySearchTree
from timer import Timer
from typing import List


# ------------------------------------------------------------------------
# Lab 9 Task 3
# ------------------------------------------------------------------------

def profile_bst(lst: List) -> None:
    """Print the time an empty BinarySearchTree takes to insert items from
    <lst>, and the time it takes to then delete items from <lst>.

    Note: you'll need to first create your own BinarySearchTree here,
    and then call insert and delete on it.
    """
    # TODO: implement this function!
    # Note: first, insert ALL the items in <lst> into an empty BST.
    # Then, delete them all.
    pass


if __name__ == '__main__':
    # Limit the depth of recursion to a level greater than is needed
    # for this lab exercise.  This will prevent incorrect code that has
    # infinite recursion from crashing Python.
    sys.setrecursionlimit(10000)

    sizes = [500, 1000, 2000, 4000]

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from a sorted list of that size.
    print('--- Sorted ---')
    for size in sizes:
        sorted_list = list(range(size))
        profile_bst(sorted_list)

    # For each of a series of list sizes, time insertion and deletion
    # into a bst from an UNsorted list of that size.
    print('\n--- Random ---')
    for size in sizes:
        random_list = list(range(size))
        random.shuffle(random_list)
        profile_bst(random_list)
