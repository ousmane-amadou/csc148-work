"""Lab 6: Linked List Exercises, Part 2

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the code for a linked list implementation with two classes,
LinkedList and _Node.

All of the code from lecture is here, as well as some exercises to work on.
"""
from typing import Optional, Callable, Iterator, Union


class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one which is only meant
    to be used in this module by the LinkedList class, but not by client code.

    === Attributes ===
    item:
        The data stored in this node.
    next:
        The next node in the list, or None if there are no more nodes.
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
    # _iter_node:
    #     The current location of the iterator.
    #     (Used for an additional exercise.)
    _first: Optional[_Node]
    _iter_node: Optional[_Node]

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

        # Initialize a node for the iterator
        self._iter_node = None

    # ------------------------------------------------------------------------
    # Non-mutating methods: these methods do not change the list
    # ------------------------------------------------------------------------
    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> LinkedList([]).is_empty()
        True
        >>> LinkedList([1, 2, 3]).is_empty()
        False
        """
        return self._first is None

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

    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedList([])
        >>> len(lst)              # Equivalent to lst.__len__()
        0
        >>> lst = LinkedList([1, 2, 3])
        >>> len(lst)
        3
        """
        curr = self._first
        size = 0
        while curr is not None:
            size += 1
            curr = curr.next
        return size

    def __getitem__(self, index: int) -> Union[object, 'LinkedList']:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.

        >>> linky = LinkedList([100, 4, -50, 13])
        >>> linky[0]          # Equivalent to linky.__getitem__(0)
        100
        >>> linky[2]
        -50
        >>> linky[100]
        Traceback (most recent call last):
        IndexError
        """
        curr = self._first
        curr_index = 0

        # Iterate to (index)-th node
        # Note: the two STOPPING conditions are
        # (1) curr is None (gone past the end of the list)
        # (2) curr_index == index (reached the correct node)
        # The loops stops when (1) or (2) is true,
        # so it *continues* when both are false.
        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise IndexError
        else:
            return curr.item

    # ------------------------------------------------------------------------
    # Mutating methods: these methods modify the list
    # ------------------------------------------------------------------------
    def pop(self, index: int) -> object:
        """Remove and return the item at position <index>.

        Raise IndexError if index >= len(self) or index < 0.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.pop(1)
        2
        >>> lst.pop(2)
        200
        >>> lst.pop(148)
        Traceback (most recent call last):
        IndexError
        >>> lst.pop(0)
        1
        """
        if index == 0:
            item, self._first = self._first.item, self._first.next
            return item
        else:
            # Iterate to (index-1)-th node.
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None or curr.next is None:
                raise IndexError
            else:
                # Update link to skip over i-th node
                item, curr.next = curr.next.item, curr.next.next
                return item

    def insert(self, index: int, item: object) -> None:
        """Insert a new node containing item at position <index>.

        Raise IndexError if index > len(self) or index < 0.
        Note that adding to the end of a linked list is okay.

        >>> lst = LinkedList([1, 2, 10, 200])
        >>> lst.insert(2, 300)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200]'
        >>> lst.insert(5, -1)
        >>> str(lst)
        '[1 -> 2 -> 300 -> 10 -> 200 -> -1]'
        >>> lst.insert(100, 2)
        Traceback (most recent call last):
        IndexError
        """
        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            self._first, new_node.next = new_node, self._first
        else:
            # Iterate to (index-1)-th node.
            curr = self._first
            curr_index = 0
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                # Update links to insert new node
                curr.next, new_node.next = new_node, curr.next

    def remove(self, item: object) -> None:
        """Remove the FIRST occurrence of <item> in this list.

        Do nothing if this list does not contain <item>.
        (Note: Python lists actually raise a ValueError.)

        >>> lst = LinkedList([1, 2, 3])
        >>> lst.remove(2)
        >>> str(lst)
        '[1 -> 3]'
        >>> lst.remove(2)
        >>> str(lst)
        '[1 -> 3]'
        >>> lst.remove(3)
        >>> str(lst)
        '[1]'
        >>> lst.remove(1)
        >>> str(lst)
        '[]'
        >>> lst.remove(1)
        >>> str(lst)
        '[]'
        """
        # NOTE: Implement without using any other methods.

        # Find the node.
        prev = None
        curr = self._first
        while curr is not None and curr.item != item:
            prev, curr = curr, curr.next

        # Delete the node, carefully.
        if curr is not None:
            if prev is not None:
                prev.next = curr.next
            else:
                self._first = curr.next

    def clear(self) -> None:
        """Remove all items from this list.

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        >>> lst.clear()
        >>> str(lst)
        '[]'
        """
        pass

    def append(self, item: object) -> None:
        """Append <item> to the end of this list.

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        >>> lst.append(4)
        >>> str(lst)
        '[1 -> 2 -> 3 -> 4]'
        """
        pass

    def __setitem__(self, index: int, item: object) -> None:
        """Store item at position <index> in this list.

        Raise IndexError if index is >= the length of self.

        >>> lst = LinkedList([1, 2, 3])
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        """
        pass

    def extend(self, items: list) -> None:
        """Extend this list by appending elements from <items>.

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        >>> lst.extend([4, 5, 6, 7])
        >>> str(lst)
        '[1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7]'
        """
        pass

    def map(self, f: Callable[[object], object]) -> 'LinkedList':
        """Return a new LinkedList whose nodes store items that are
        obtained by applying f to each item in this linked list.

        Do not change this linked list.

        For extra practice, do not store items in a Python list; instead,
        use only the LinkedList and _Node classes.

        >>> func = str.upper
        >>> func('hi')
        'HI'
        >>> lst = LinkedList(['Hello', 'Goodbye'])
        >>> str(lst.map(func))
        '[HELLO -> GOODBYE]'
        >>> str(lst.map(len))
        '[5 -> 7]'
        """
        pass

    def filter(self, f: Callable[[object], bool]) -> 'LinkedList':
        """Return a new LinkedList whose nodes store the items in this
        linked list that make f return True.

        Do not change this linked list.

        For extra practice, do not store items in a Python list; instead,
        use only the LinkedList and _Node classes.

        >>> func = str.islower
        >>> func('hi')
        True
        >>> func('Hi')
        False
        >>> lst = LinkedList(['Hello', 'goodbye', 'see you later'])
        >>> str(lst.filter(func))
        '[goodbye -> see you later]'
        """
        pass

    ###########################################################################
    # Additional Exercises
    ###########################################################################
    def __iter__(self) -> Iterator['LinkedList']:
        """Return a linked list iterator.

        Hint: the easiest way to implement __iter__ and __next__ is to
        make the linked list object responsible for its own iteration.

        In other words, __iter__(self) should simply return <self>.
        However, in order to make sure the loop always starts at the beginning
        of the list, you'll need the new private attribute for this class which
        keeps track of where in the list the iterator is currently at.
        """

        return self

    def __next__(self) -> object:
        """Return the next item in the iteration.

        Raise StopIteration if there are no more items to return.

        Hint: If you have an attribute keeping track of the where the iteration
        is currently at in the list, it should be straightforward to return
        the current item, and update the attribute to be the next node in
        the list.

        >>> lst = LinkedList([1, 2, 3])
        >>> iterator = lst.__iter__()
        >>> iterator.__next__()
        1
        >>> iterator.__next__()
        2
        >>> iterator.__next__()
        3
        """
        if self._iter_node.next is None:
            raise StopIteration
        else:
            self._iter_node = self._iter_node.next

        return self._iter_node


if __name__ == '__main__':
    pass
