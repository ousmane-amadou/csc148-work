"""Lab 7: Recursion, Task 2

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a new *recursive* implementation of the List ADT
called LinkedListRec. Study it carefully, and then try implementing the
methods in this class.
"""

from typing import Optional, List, Callable

class LinkedListRec:
    """A recursive linked list implementation of the List ADT.

    Note the structural differences between this implementation
    and the node-based implementation from the past few weeks.
    Even though both classes have the same public interface,
    how they implement their methods are quite different!

    This implementation does not require a "_Node" class.
    """
    # === Private Attributes ===
    # _first:
    #     The first item in the list.
    # _rest:
    #     A list containing the items that come after
    #     the first one.
    _first: Optional[object]
    _rest: Optional['LinkedListRec']

    # === Representation Invariants ===
    # _first is None if and only if _rest is None.
    #     This represents an empty list.

    def __init__(self, items: List) -> None:
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.
        """
        if len(items) == 0:
            self._first = None
            self._rest = None
        else:
            self._first = items[0]
            self._rest = LinkedListRec(items[1:])

    def is_empty(self) -> bool:
        """Return whether this linked list is empty.

        >>> lst1 = LinkedListRec([])
        >>> lst1.is_empty()
        True
        >>> lst2 = LinkedListRec([1, 2, 3])
        >>> lst2.is_empty()
        False
        """
        return (self._first is None)

    def __str__(self) -> str:
        """Return a string representation of this list..

        >>> lst = LinkedListRec([1, 2, 3])
        >>> str(lst) # Equivalent to lst.__str__()
        '1 -> 2 -> 3'
        """
        if self.is_empty():
            return ''
        elif self._rest.is_empty():
            return str(self._first)
        else:
            return str(self._first) + ' -> ' + str(self._rest)

    def __len__(self) -> int:
        """Return the number of elements in this list.

        >>> lst = LinkedListRec([])
        >>> len(lst) # Equivalent to lst.__len__()
        0
        >>> lst = LinkedListRec([1, 2, 3])
        >>> len(lst)
        3
        """
        if self.is_empty():
            return 0
        else:
            return 1 + len(self._rest)

    def __getitem__(self, index: int) -> object:
        """Return the item at position <index> in this list.

        Raise IndexError if <index> is >= the length of this list.

        >>> lst = LinkedListRec([1, 2, 3])
        >>> lst[0] # Equivalent to lst.__getitem__(0)
        1
        >>> lst[1]
        2
        >>> lst[2]
        3
        >>> lst[3]
        Traceback (most recent call last):
        ...
        IndexError
        """
        if self._first is None:
            raise IndexError

        if index == 0:
            return self._first
        else:
            return self._rest.__getitem__(index-1)

    def __setitem__(self, index: int, item: object):
        """Store item at position <index> in this list.

        Raise IndexError if index is >= the length of <self>.

        >>> lst = LinkedListRec([1, 2, 3])
        >>> lst[0] = 100 # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> lst[3] = 400
        Traceback (most recent call last):
        ...
        IndexError
        >>> str(lst)
        '100 -> 200 -> 300'
        """
        if self._first is None:
            raise IndexError

        if index == 0:
            self._first = item
        else:
            return self._rest.__setitem__(index-1, item)

    def __contains__(self, item: object) -> bool:
        """Return whether <item> is in this list.

        Use == to compare items.

        >>> lst = LinkedListRec([1, 2, 3])
        >>> 2 in lst # Equivalent to lst.__contains__(2)
        True
        >>> 4 in lst
        False
        """
        if self._first == item:
            return True
        elif self._first == None:
            return False
        else:
            return self._rest.__contains__(item)

    def count(self, item: object) -> int:
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        >>> lst = LinkedListRec([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        if self._first == item:
            return 1 + self._rest.count(item)
        elif self._first == None:
            return 0
        else:
            return self._rest.count(item)


    # ------------------------------------------------------------------------
    # Mutating methods: these methods modify the structure of the list
    # ------------------------------------------------------------------------
    def pop_first(self) -> None:
        """Remove the first item in the list.

        Raise an IndexError if the list is empty.

        >>> lst = LinkedListRec([1, 2, 3])
        >>> lst.pop_first()
        >>> str(lst)
        '2 -> 3'
        >>> lst.pop_first()
        >>> str(lst)
        '3'
        >>> lst.pop_first()
        >>> str(lst)
        ''
        """
        self._first = self._rest._first
        self._rest = self._rest._rest

    def insert_first(self, item: object) -> None:
        """Insert item at the front of the list.

        This should work even if the list is empty.

        >>> lst = LinkedListRec([])
        >>> lst.insert_first(3)
        >>> str(lst)
        '3'
        >>> lst.insert_first(2)
        >>> str(lst)
        '2 -> 3'
        >>> lst.insert_first(1)
        >>> str(lst)
        '1 -> 2 -> 3'
        """
        rest = LinkedListRec([self._first])
        rest._rest = self._rest

        self._first = item
        self._rest = rest


    def pop(self, index: int) -> None:
        """Remove node at position <index>.

        Raise IndexError if <index> is >= the length of this list.

        >>> lst = LinkedListRec([1, 2, 3])
        >>> lst.pop(2)
        >>> str(lst)
        '1 -> 2'
        >>> lst.pop(1)
        >>> str(lst)
        '1'
        >>> lst.pop(0)
        >>> str(lst)
        ''
        >>> lst.pop(0)
        Traceback (most recent call last):
        ...
        IndexError
        """
        if self._first is None:
            raise IndexError
        elif index == 0:
            self.pop_first()
        else:
            self._rest.pop(index-1)

    def insert(self, index: int, item: object) -> None:
        """Insert item in to the list at position <index>.

        Raise an IndexError if index is > the length of the list.
        Note that it is possible to add to the end of the list
        (when index == len(self)).

        >>> lst = LinkedListRec(['c'])
        >>> lst.insert(0, 'a')
        >>> str(lst)
        'a -> c'
        >>> lst.insert(1, 'b')
        >>> str(lst)
        'a -> b -> c'
        >>> lst.insert(3, 'd')
        >>> str(lst)
        'a -> b -> c -> d'
        >>> lst.insert(5, 'd')
        Traceback (most recent call last):
        ...
        IndexError
        """
        if index == 0:
            self.insert_first(item)
        elif self._first is None:
            raise IndexError
        else:
            self._rest.insert(index-1, item)

    # --- Additional Exercises ---

    def map(self, f: Callable[[object], object]) -> 'LinkedListRec':
        """Return a new LinkedList whose nodes store items that are
        obtained by applying f to each item in this linked list.

        Does not change this linked list.

        >>> func = str.upper
        >>> func('hi')
        'HI'
        >>> lst = LinkedListRec(['Hello', 'Goodbye'])
        >>> str(lst.map(func))
        'HELLO -> GOODBYE'
        >>> str(lst.map(len))
        '5 -> 7'
        """
        new_LLR = LinkedListRec([])

        c = 0
        curr = self
        while curr._first is not None:
            new_LLR.insert(c, f(curr._first))
            curr = curr._rest
            c += 1
        return new_LLR
