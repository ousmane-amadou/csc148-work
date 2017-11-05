"""CSC148 Exercise 5: Tree Practice

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 5.

NOTE: the hypothesis tests here use some helper functions to create
random instances of the data types we want (trees and binary trees).
We've provided helper functions to do this---you don't need to
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
import unittest
from hypothesis import given, assume
from hypothesis.strategies import integers, lists, recursive, builds, just

from ex5 import Tree, to_tree, BinaryTree


##############################################################################
# Helper functions and custom Hypothesis strategies for generating inputs
##############################################################################
def _binary_tree_size(bt: BinaryTree) -> int:
    """Return the size of the given binary tree.
    """
    if bt.is_empty():
        return 0
    else:
        return 1 + _binary_tree_size(bt._left) + _binary_tree_size(bt._right)


def _tree_size(t: Tree) -> int:
    """Return the size of the given tree.
    """
    if t.is_empty():
        return 0
    else:
        s = 1
        for subtree in t._subtrees:
            s += _tree_size(subtree)
        return s


def item():
    """Generate an integer between -10000 and 10000."""
    return integers(min_value=-10000, max_value=10000)


def single_root():
    """Generate a tree with a single node.

    The root value is an integer between -10000 and 10000.
    """
    return builds(Tree,
                  root=item(),
                  subtrees=just([]))


def trees():
    """Generate a non-empty tree with integer items between -10000 and 10000."""
    return recursive(single_root(),
                     lambda children:
                         builds(Tree,
                                root=item(),
                                subtrees=lists(children)))


def bt_empty():
    """Generate an empty BinaryTree."""
    return just(BinaryTree(None, None, None))


def binary_trees():
    """Generate a BinaryTree with integer items between -10000 and 10000."""
    return recursive(bt_empty(),
                     lambda s: builds(BinaryTree, root=item(), left=s, right=s))


##############################################################################
# The actual tests
##############################################################################
@given(trees())
def test_tree_equals_itself(tree):
    """Test that a tree always equals itself."""
    assert tree == tree


def test_empty():
    """Test __eq__ with empty trees."""
    tree1 = Tree(1, [])
    tree_emp = Tree(None, [])
    tree_emp2 = Tree(None, [])
    assert tree_emp != tree1
    assert tree1 != tree_emp
    assert tree_emp == tree_emp2


def test_to_nested_list_one():
    """Test to_nested_list on a tree with size one."""
    t = Tree(1, [])
    assert t.to_nested_list() == [1]


def test_to_nested_list_line():
    """Test to_nested_list on a tree with a linear structure."""
    t5 = Tree(5, [])
    t4 = Tree(4, [t5])
    t3 = Tree(3, [t4])
    t2 = Tree(2, [t3])
    t1 = Tree(1, [t2])

    assert t1.to_nested_list() == [1, [2, [3, [4, [5]]]]]


def test_to_tree_one():
    """Test to_tree on a nested list with one element."""
    t = to_tree([1])
    assert t._root == 1
    assert t._subtrees == []


def test_line():
    """Test to_tree given a tree with height 2."""
    t = to_tree([10, [2], [4], [5], [3]])
    assert t._root == 10
    assert t._subtrees[0]._root == 2
    assert t._subtrees[1]._root == 4
    assert t._subtrees[2]._root == 5
    assert t._subtrees[3]._root == 3
    assert _tree_size(t) == 5


def test_orders_empty():
    """Test binary tree orderings when given an empty tree."""
    btree = BinaryTree(None, None, None)
    assert btree.preorder() == []
    assert btree.postorder() == []
    assert btree.inorder() == []


@given(binary_trees())
def test_root_position(btree):
    """Test preorder and postorder positioning of the tree root."""
    assume(not btree.is_empty())
    assert btree.preorder()[0] == btree._root
    assert btree.postorder()[-1] == btree._root


@given(binary_trees())
def test_orders_have_correct_length(btree):
    """Test that the binary tree orderings have the correct length."""
    pre_len = len(btree.preorder())
    in_len = len(btree.inorder())
    post_len = len(btree.postorder())
    assert pre_len == _binary_tree_size(btree)
    assert in_len == _binary_tree_size(btree)
    assert post_len == _binary_tree_size(btree)


if __name__ == '__main__':
    import pytest
    pytest.main()
