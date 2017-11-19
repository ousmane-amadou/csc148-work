"""CSC148 Exercise 6: Binary Search Trees

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 6.

NOTE: the hypothesis tests here use some helper functions to create
random instances of the data types we want (binary search trees).
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
from hypothesis import given, settings
from hypothesis.strategies import integers, lists, builds
from ex6 import BinarySearchTree


##############################################################################
# Helper functions and custom Hypothesis strategies for generating inputs
##############################################################################
def _list_to_bst(items: list) -> 'BinarySearchTree':
    bst = BinarySearchTree(None)
    for item in items:
        bst.insert(item)
    return bst


def bsts():
    """Return a hypothesis strategy to generate BSTs.

    This builds a BST containing between 10 and 60 integers.
    """
    return builds(_list_to_bst,
                  items=lists(integers(min_value=-10000, max_value=10000),
                              min_size=10, max_size=60))


##############################################################################
# The actual tests
##############################################################################
@given(integers(max_value=10000))
def test_num_less_than_leaf(root):
    """Test num_less_than on a BST with a single item."""
    bst = BinarySearchTree(root)
    assert bst.num_less_than(root + 3) == 1
    assert bst.num_less_than(root - 3) == 0
    assert bst.num_less_than(root) == 0  # Pay attention to this one!


@given(lists(integers(min_value=-10000, max_value=10000),
             min_size=10, max_size=60))
def test_num_less_than_bigger(items):
    """Test num_less_than on a larger BST."""
    bst = _list_to_bst(items)
    print(bst)
    print(bst.num_less_than(max(items) + 1))
    assert bst.num_less_than(min(items) - 1) == 0
    assert bst.num_less_than(min(items)) == 0
    assert bst.num_less_than(max(items) + 1) == len(items)


@given(integers())
def test_items_at_depth_leaf(root):
    """Test items_at_depth on a BST with a single item."""
    bst = BinarySearchTree(root)
    assert bst.items_at_depth(1) == [root]  # The root is at depth 1.
    assert bst.items_at_depth(2) == []


@given(bsts())
def test_items_at_depth_one(bst):
    """Test items_at_depth for the root level (d=1)."""
    # Note that we're accessing a private attribute here.
    # This is a little unusual for a test, but suits our purposes
    # for this exercise, which is all about manipulating BSTs.
    assert bst.items_at_depth(1) == [bst._root]


@given(integers())
@settings(max_examples=10)
def test_levels_leaf(root):
    """Test levels on a BST with a single item."""
    bst = BinarySearchTree(root)
    assert bst.levels() == [(1, [root])]


@given(bsts())
@settings(max_examples=10)
def test_levels_correct_length(bst):
    """Test levels returns a list with the correct length."""
    assert len(bst.levels()) == bst.height()


if __name__ == '__main__':
    import pytest
    pytest.main()
