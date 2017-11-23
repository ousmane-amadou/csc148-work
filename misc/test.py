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
