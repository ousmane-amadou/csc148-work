"""CSC148 Exercise 4: Recursion Practice

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 4.

NOTE: the hypothesis tests here use some helper functions to create
random instances of the data types we want (nested list and Person).
We've provided helper functions to do this -- you don't need to
understand how they work, but we do encourage you to use them to
write your own hypothesis tests.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<http://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
from hypothesis import given
from hypothesis.strategies import integers, lists, recursive, builds, text, just

from ex4 import duplicate, add_one, Person


##############################################################################
# Helper functions
##############################################################################
def num_ints(nested_list):
    """Return the number of integers in a nested list."""
    if isinstance(nested_list, int):
        return 1
    else:
        s = 0
        for obj in nested_list:
            s += num_ints(obj)
        return s


def num_lists(nested_list):
    """Return the number of lists in a nested list (including itself)."""
    if isinstance(nested_list, int):
        return 0
    else:
        s = 1
        for x in nested_list:
            if isinstance(x, list):
                s += 1
        return s


# The following three helpers are for generating hypothesis test inputs.
# You certainly *don't* need to understand how they are implemented,
# but you may find them very useful in writing your own hypothesis tests.
def nested_lists():
    """Generate a nested list (for hypothesis tests).

    Example usage:

    @given(nested_lists())
    def test_something(nested_list):
        ...
    """
    return recursive(integers(), lists)


def person_no_children():
    """Generate a Person with no children (for hypothesis tests).

    Example usage:

    @given(person_no_children())
    def test_something(input_person):
        ...
    """
    return builds(Person, new_name=text(), new_children=just([]))


def person():
    """Generate a Person (who may or may not have children).

    This is recursive, and can generate quite large family trees.

    Example usage:

    @given(person())
    def test_something(input_person):
        ...
    """
    return recursive(person_no_children(),
                     lambda x: builds(Person, new_name=text(),
                                      new_children=lists(x)))


##############################################################################
# Task 1: More practice with nested lists
##############################################################################
@given(integers())
def test_handles_integers(x):
    """Test duplicate when given an integer."""
    assert duplicate(x) == [x, x]


@given(nested_lists())
def test_twice_as_many_ints(x):
    """Test the number of integers resulting from duplicate.
    """
    assert num_ints(duplicate(x)) == 2 * num_ints(x)


def test_duplicate_doctest():
    """Test the doctest example for duplicate."""
    nested_list = [1, [2, 3]]
    expected = [1, 1, [2, 2, 3, 3]]
    assert duplicate(nested_list) == expected


@given(lists(integers()))
def test_list_of_ints(nested_list):
    """Test add_one on a list of ints."""
    copy = nested_list[:]  # create a copy of the input
    add_one(copy)
    for i in range(len(nested_list)):
        assert copy[i] == nested_list[i] + 1


def test_add_one_doctest():
    """Test the doctest example for add_one."""
    nested_list = [1, [2, 3], [[[5]]]]
    expected = [2, [3, 4], [[[6]]]]
    add_one(nested_list)
    assert nested_list == expected


@given(nested_lists())
def test_same_number_of_lists_and_ints(x):
    """Test that add_one keeps the number of ints and lists the same."""
    old_num_lists = num_lists(x)
    old_num_ints = num_ints(x)
    add_one(x)
    assert num_lists(x) == old_num_lists
    assert num_ints(x) == old_num_ints


##############################################################################
# Task 2: Family trees
##############################################################################
@given(person_no_children())
def test_person_with_no_children(p):
    """Test count_descendants on a person with no children."""
    assert p.count_descendants() == 0


@given(text(), lists(person_no_children()))
def test_person_with_some_children(name, children):
    """Test count_descendants on a person with some children.

    Each child has *no* children of their own in this test case.
    """
    # children is a list of Person objects, each of whom have no children
    p = Person(name, children)

    # The number of descendants of p is equal to their number of children
    assert p.count_descendants() == len(children)


def test_small_family():
    """Test count_descendants on a small example."""
    aura = Person('aura', [])
    zane = Person('zane', [])
    goku = Person('goku', [aura, zane])
    mina = Person('mina', [goku])
    assert mina.count_descendants() == 3


if __name__ == '__main__':
    import pytest
    pytest.main()
