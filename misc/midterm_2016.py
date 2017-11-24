"""

"""

from typing import Optional, Callable, List

class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are
        no more nodes in the list.
    """
    item: object
    next: Optional['_Node']

    def __init__(self, item: object) -> None:
        """Initialize a new node storing <item>, with no next node.
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # _first:
    #     The first node in the linked list, or None if the list is empty.
    _first: Optional[_Node]

    def __init__(self, items: list) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = _Node(item)
                current_node = current_node.next

    def __str__(self) -> str:
        """Return a string representation of this list in the form
        '[item1 -> item2 -> ... -> item-n]'.

        >>> str(LinkedList([1, 2, 3]))
        '[1 -> 2 -> 3]'
        >>> str(LinkedList([]))
        '[]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    def remove_first_double(self) -> None:
        """
        Remove second of two adjacent nodes with duplicate values.
        If there is no such node, leave self as is. No need
        to deal with subsequent adjacent duplicate values.

        >>> ll = LinkedList([1, 2, 2, 2, 3])
        >>> ll.remove_first_double()
        >>> str(ll)
        '[1 -> 2 -> 2 -> 3]'
        >>> ll = LinkedList([1, 1])
        >>> ll.remove_first_double()
        >>> str(ll)
        '[1]'
        """
        if self._first is None:
            return
        prev = self._first
        curr = self._first.next
        while curr is not None:
            if prev.item == curr.item:
                prev.next = curr.next
                return
            prev = prev.next
            curr = curr.next

# MY SOLUTION
def contains_satisfier(list_: list, predicate: Callable) -> bool:
    """
    Return whether possibly-nested list_ contains a non-list element
    that satisfies (returns True for) predicate.

    >>> list_ = [5, [6, [7, 8]], 3]
    >>> def p(n): return n > 7
    >>> contains_satisfier(list_, p)
    True
    >>> def p(n): return n > 10
    >>> contains_satisfier(list_, p)
    False
    """
    if isinstance(list_, int):
        return predicate(list_)
    else:
        for item in list_:
            if contains_satisfier(item, predicate):
                return True
        return False

# OFFICIAL SOLUTION
def contains_satisfier_2(list_: list, predicate: Callable) -> bool:
    return any([contains_satisfier(c, predicate) if isinstance(c, list) else predicate(c)
                for c in list_])
class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and LinkedListRec
    from Lab 7; the only major difference is that _rest
    has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[object]
    # The list of all subtrees of this tree.
    _subtrees: List['Tree']

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty Tree.
    # - self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    def __init__(self, root: object, subtrees: List['Tree']) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

# MY SOLUTION
def count_odd_above(t: Tree, n: int) -> int:
    """
    Return the number of nodes with depth less than n that have odd values.
    Assume t’s nodes have integer values.

    >>> t1 = Tree(4, [])
    >>> t2 = Tree(3, [])
    >>> t3 = Tree(5, [t1, t2])
    >>> count_odd_above(t3, 1)
    1
    """
    if n <= 0:
        return 0
    else:
        count = 0 if (n % 2) == 0 else 1
        for tree in t._subtrees:
            count += count_odd_above(tree, n-1)
        return count

# OFFICIAL SOLUTION
def count_odd_above_2(t: Tree, n: int) -> int:
    """
    Return the number of nodes with depth less than n that have odd values.
    Assume t’s nodes have integer values.

    >>> t1 = Tree(4, [])
    >>> t2 = Tree(3, [])
    >>> t3 = Tree(5, [t1, t2])
    >>> count_odd_above(t3, 1)
    1
    """
    if n <= 0:
        return 0
    else:
        return ((1 if t.value % 2 == 1 else 0) +
                sum([count_odd_above(c, n - 1) for c in t.children]))
