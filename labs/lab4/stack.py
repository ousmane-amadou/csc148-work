"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will write two different functions that
operate on a Stack, paying attention to whether or not the queue should be
modified.
"""
from typing import Generic, List, TypeVar


# Ignore this line; it is only used to facilitate PyCharm's typechecking.
T = TypeVar('T')


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


class EmptyStackError(Exception):
    """Exception raised when an error occurs."""
    pass

def size(s: Stack) -> int:
    """Return the number of items in s.

    Do not mutate s.

    >>> s = Stack()
    >>> size(s)
    0
    >>> s.push('hi')
    >>> s.push('more')
    >>> s.push('stuff')
    >>> size(s)
    3
    """
    side_stack = Stack()
    count = 0
    # Pop everything off <s> and onto <side_stack>, counting as we go.
    while not s.is_empty():
        side_stack.push(s.pop())
        count += 1
    # Now pop everything off <side_stack> and back onto <s>.
    while not side_stack.is_empty():
        s.push(side_stack.pop())
    # <s> is restored to its state at the start of the function call.
    # We consider that it was not mutated.
    return count


def remove_big(stack: Stack[int]) -> None:
    """Remove the items in <stack> that are greater than 5.

    Do not change the relative order of the other items.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> s.push(8)
    >>> s.push(4)
    >>> remove_big(s)
    >>> s.pop()
    4
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    """
    # Stack that holds all the items less than or equal to 5, in reverse order
    remaining_elem = Stack()

    while not stack.is_empty():
        top = stack.pop()
        if top <= 5:
            remaining_elem.push(top)

    while not remaining_elem.is_empty():
        stack.push(remaining_elem.pop())


def double_stack(stack: Stack) -> Stack:
    """Return a new stack that contains two copies of every item in <stack>.

    We'll leave it up to you to decide what order to put the copies into in
    the new stack.

    >>> s = Stack()
    >>> s.push(1)
    >>> s.push(29)
    >>> new_stack = double_stack(s)
    >>> s.pop()  # s should be unchanged.
    29
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    >>> new_items = []
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> new_items.append(new_stack.pop())
    >>> sorted(new_items)
    [1, 1, 29, 29]
    """

    tmp_stack = Stack()
    new_stack = Stack()
    while not stack.is_empty():
        top = stack.pop()
        tmp_stack.push(top)
        new_stack.push(top)

    while not tmp_stack.is_empty():
        top = stack.pop()
        stack.push(top)
        new_stack.push(top)

    return new_stack

if __name__ == '__main__':
    import doctest
    doctest.testmod()
