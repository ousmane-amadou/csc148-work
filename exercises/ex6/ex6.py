"""CSC148 Exercise 6: Binary Search Trees Practice

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for Exercise 6.

You are responsible for completing three BinarySearchTree methods in this file.

Note: there's only one Task for this exercise.
"""
from typing import List, Optional, Tuple


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every node, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[object]
    # The left subtree, or None if the tree is empty
    _left: Optional['BinarySearchTree']
    # The right subtree, or None if the tree is empty
    _right: Optional['BinarySearchTree']

    # === Representation Invariants ===
    #  - If _root is None, then so are _left and _right.
    #    This represents an empty BST.
    #  - If _root is not None, then _left and _right are BinarySearchTrees.
    #  - (BST Property) All items in _left are <= _root,
    #    and all items in _right are >= _root.

    def __init__(self, root: Optional[object]) -> None:
        """Initialize a new BST with the given root value and no children.

        If <root> is None, make an empty tree, with subtrees that are None.
        If <root> is not None, make a tree with subtrees are empty trees.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def __contains__(self, item: object) -> bool:
        """Return True if <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left   # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    def height(self) -> int:
        """Return the height of this BST.

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        if self.is_empty():
            return 0
        else:
            return max(self._left.height(), self._right.height()) + 1

    def insert(self, item: object) -> None:
        """Insert <item> into this BST, maintaining the BST property.

        Do not change positions of any other nodes.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        if self.is_empty():
            # Make new leaf node.
            # Note that self._left and self._right cannot be None if the
            # tree is non-empty! (This is one of our invariants.)
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item <= self._root:
            self._left.insert(item)
        else:
            self._right.insert(item)


##############################################################################
# Task 1: More BST practice
##############################################################################
    def num_items(self) -> int:
        """Return the number of items in <tree>.
        """
        if self.is_empty():
            return 0
        else:
            return 1 + self._right.num_items() + self._left.num_items()

    def num_less_than(self, item: object) -> int:
        """Return the number of items in this BST that are less than <item>.
        """
        if self._root is None:
            return 0
        else:
            if self._root < item:
                return 1 + self._right.num_items() + self._left.num_items()
            else:
                return self._left.num_less_than(item)

    def items_at_depth(self, d: int) -> list:
        """Return a sorted list of all items in this BST at depth <d>.

        Precondition: d >= 1.

        Reminder: you should not have to use the built-in 'sort' method
        or do any sorting yourself.
        """

        if self.is_empty():
            return []
        else:
            if d == 1:
                return [self._root]
            else:
                return self._left.items_at_depth(d-1) \
                       + self._right.items_at_depth(d-1)

    def levels(self) -> List[Tuple[int, list]]:
        """Return a list of items in the tree, separated by level.

        You may wish to use 'items_at_depth' as a helper method,
        but this also makes your code less efficient. Try doing
        this method twice, once with 'items_at_depth', and once
        without it!
        """
        if self.is_empty():
            return []
        else:
            llevels = self._left.levels()
            rlevels = self._right.levels()
            clevels = [(1, [self._root])]

            min_depth = min(len(llevels), len(rlevels))
            max_depth = max(len(llevels), len(rlevels))

            left_deeper = len(llevels) > len(rlevels)

            if len(llevels) + len(rlevels) == 0:
                return clevels

            for i in range(0, max_depth):
                if (i >= min_depth) and left_deeper:
                    depth = 1 + llevels[i][0]
                    items = llevels[i][1]
                elif (i >= min_depth) and not left_deeper:
                    depth = 1 + rlevels[i][0]
                    items = rlevels[i][1]
                else:
                    depth = 1 + rlevels[i][0]
                    items = llevels[i][1] + rlevels[i][1]
                clevels.append((depth, items))

            return clevels


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
