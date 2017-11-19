"""Lab 9: Binary Search Trees

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few BinarySearchTree methods that you will implement.
Make sure you understand the *BST Property*; it will play an important role
in several of these methods.
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

    def __str__(self):
        """Return a str containing all of the items in this BST, using
        indentation to show depth.
        """
        # Remove the final newline.
        return self._str_indented(0)[:-1]

    def _str_indented(self, depth: int) -> str:
        """Return a str containing all of the items in this BST, indented
        <depth> steps.
        """
        if self.is_empty():
            return ""
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

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

    # ------------------------------------------------------------------------
    # Lab 9 Task 1
    # ------------------------------------------------------------------------
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
        if self._root is None:
            return 0
        else:
            return 1 + max(self._left.height(), self._right.height())

    def items(self) -> List:
        """Return all of the items in the BST in sorted order.

        >>> BinarySearchTree(None).items()
        []
        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        """
        if self._root is None:
            return []
        else:
            return self._left.items() + [self._root] + self._right.items()

    def smaller(self, item: object) -> List:
        """Return all of the items in the BST strictly smaller than <item>
        in sorted order.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.smaller(6)
        [2, 3, 5]
        >>> bst.smaller(13)
        [2, 3, 5, 7, 9, 11]
        """
        if self._root is None:
            return []
        else:
            if self._root < item:
                return self._left.items() + [self._root] + self._right.smaller(item)
            else:
                return self._left.smaller(item)

    # ------------------------------------------------------------------------
    # Lab 9 Task 2
    # ------------------------------------------------------------------------
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
        if self._root is None:
            self._root = item
        else:
            if item < self._root:
                self._left.insert(item)
            else:
                self._right.insert(item)
        pass

    # ------------------------------------------------------------------------
    # Lab 9 Task 4
    # ------------------------------------------------------------------------
    def rotate_right(self) -> None:
        """Rotate the BST clockwise, i.e. make the left subtree the root.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> right = BinarySearchTree(11)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> bst._left = left
        >>> bst._right = right
        >>> print(bst)
        7
          3
            2
            5
          11
        >>> bst.rotate_right()
        >>> print(bst)
        3
          2
          7
            5
            11
        >>> bst.rotate_right()
        >>> print(bst)
        2
          3
            7
              5
              11
        """
        # Assign pivot to left subtree
        pivot = self._left
        self._left = pivot._right

        # Pivot's left subtree becomes current subtree
        pivot._right = BinarySearchTree(self._root)
        pivot._right._left = self._left
        pivot._right._right = self._right

        # Reassign self to pivot
        self._root = pivot._root
        self._left = pivot._left
        self._right = pivot._right

    def rotate_left(self) -> None:
        """Rotate the BST counter-clockwise,
        i.e. make the right subtree the root.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> print(bst)
        7
          3
            2
            5
          11
            9
            13
        >>> bst.rotate_left()
        >>> print(bst)
        11
          7
            3
              2
              5
            9
          13
        >>> bst.rotate_left()
        >>> print(bst)
        13
          11
            7
              3
                2
                5
              9
        """
        pivot = self._right
        self._right = pivot._left

        pivot._left = BinarySearchTree(self._root)
        pivot._left._left = self._left
        pivot._left._right = self._right

        self._root = pivot._root
        self._left = pivot._left
        self._right = pivot._right

    # ------------------------------------------------------------------------
    # Code to be profiled in Lab 9 Task 3
    # ------------------------------------------------------------------------

    def delete(self, item: object) -> None:
        """Remove *one* occurrence of item from this BST.

        Do nothing if <item> is not in the BST.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items()
        [2, 3, 5, 7, 9, 11, 13]
        >>> bst.delete(13)
        >>> bst.items()
        [2, 3, 5, 7, 9, 11]
        >>> bst.delete(9)
        >>> bst.items()
        [2, 3, 5, 7, 11]
        >>> bst.delete(2)
        >>> bst.items()
        [3, 5, 7, 11]
        >>> bst.delete(5)
        >>> bst.items()
        [3, 7, 11]
        >>> bst.delete(7)
        >>> bst.items()
        [3, 11]
        """
        if self.is_empty():
            pass
        elif self._root == item:
            self.delete_root()
        elif item < self._root:
            self._left.delete(item)
        else:
            self._right.delete(item)

    def delete_root(self) -> None:
        """Remove the root of this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._left.is_empty() and self._right.is_empty():
            self._root = None
            self._left = None
            self._right = None
        elif self._left.is_empty():
            self._root = self._right.extract_min()
        else:
            self._root = self._left.extract_max()

    def extract_max(self) -> object:
        """Remove and return the maximum item stored in this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._right.is_empty():
            temp = self._root
            # Copy left subtree to self, because root node is removed.
            # Note that self = self._left does NOT work!
            self._root, self._left, self._right = \
                self._left._root, self._left._left, self._left._right
            return temp
        else:
            return self._right.extract_max()

    def extract_min(self) -> object:
        """Remove and return the minimum item stored in this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._left.is_empty():
            temp = self._root
            self._root, self._left, self._right = \
                self._right._root, self._right._left, self._right._right
            return temp
        else:
            return self._left.extract_min()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
