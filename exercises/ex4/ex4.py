"""CSC148 Exercise 4: Recursion Practice

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for Exercise 4.
It is divided into two parts:
- Task 1, which contains two functions on nested lists that you should implement
  recursively, using what you've learned this week in lecture and lab.
- Task 2, which asks you to learn about a new recursive structure, a family
  tree, and write a method that operates on this structure.
"""
from typing import List, Union


##############################################################################
# Task 1: More practice with nested lists
##############################################################################
# TODO: Implement this!
def duplicate(nested_list: Union[list, int]) -> list:
    """Return a new nested list with all numbers in <nested_list> duplicated.

    Each integer in <nested_list> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <nested_list> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    if isinstance(nested_list, int):
        return [nested_list, nested_list]
    else:
        duped_list = []
        for duped_item in nested_list:
            if isinstance(duped_item, int):
                duped_list += duplicate(duped_item)
            else:
                duped_list += [duplicate(duped_item)]

        return duped_list


# TODO: Implement this!
def add_one(nested_list: Union[list, int]) -> None:
    """Add one to every number stored in <nested_list>.

    Do nothing if <nested_list> is an int.
    If <nested_list> is a list, *mutate* it to change the numbers stored.
    (Don't return anything in either case.)

    >>> lst0 = 1
    >>> add_one(lst0)
    >>> lst0
    1
    >>> lst1 = []
    >>> add_one(lst1)
    >>> lst1
    []
    >>> lst2 = [1, [2, 3], [[[5]]]]
    >>> add_one(lst2)
    >>> lst2
    [2, [3, 4], [[[6]]]]
    """
    if not isinstance(nested_list, int):

        for i in range(len(nested_list)):
            if isinstance(nested_list[i], int):
                nested_list[i] += 1
            else:
                add_one(nested_list[i])

##############################################################################
# Task 2: Family trees
##############################################################################
class Person:
    """A person in a family tree.

    === Attributes ===
    name:
        The name of this person.
    children:
        The children of this person.
    """
    name: str
    children: List['Person']

    def __init__(self, new_name: str, new_children: List['Person']) -> None:
        """Create a new person with the given name and children.
        """
        self.name = new_name
        self.children = new_children

    # TODO: Implement this!
    def count_descendants(self) -> int:
        """Return the number of descendants of this person.
        """
        pass


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()

    import doctest
    doctest.testmod()
