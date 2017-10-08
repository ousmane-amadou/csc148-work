"""CSC148 Stack Implementation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains an implementation of a Stack, together with a custom error
called EmptyStackError, used when pop is called on an empty stack.

NOTE: We've made this Stack class a "generic" type---more on this in
Wednesday's lecture.
"""
from typing import Generic, List, TypeVar


class EmptyStackError(Exception):
    """Error raised when an error occurs."""
    pass


# Ignore this line; it is only used to facilitate PyCharm's typechecking.
T = TypeVar('T')


###############################################################################
# Stacks
###############################################################################
class Stack(Generic[T]):
    """A last-in-first-out (FIFO) stack of items.

    Stores data in a first-in, last-out order. When removing an item from the
    stack, the most recently-added item is the one that is removed.
    """
    # === Private Attributes ===
    # _items:
    #     The items stored in the stack. The end of the list represents
    #     the top of the stack.
    _items: List[T]

    def __init__(self) -> None:
        """Initialize a new empty stack.
        """
        self._items = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items.

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.push('hello')
        >>> s.is_empty()
        False
        """
        return len(self._items) == 0

    def push(self, item: T) -> None:
        """Add a new element to the top of this stack.
        """
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the element at the top of this stack.

        Raise an EmptyStackError if the stack is empty.
        >>> s = Stack()
        >>> s.push('hello')
        >>> s.push('goodbye')
        >>> s.pop()
        'goodbye'
        """
        if self.is_empty():
            raise EmptyStackError
        else:
            return self._items.pop()

    # NOTE: We removed the "property" part because we were trying
    # to be too clever for our own good.
    # But still don't access _items outside of the Stack class! :)
