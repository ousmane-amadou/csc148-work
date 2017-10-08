"""CSC148 Exercise 3: Stacks and a Chain of People

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 3.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<http://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
from typing import List
from hypothesis import given
from hypothesis.strategies import lists, text, integers
from pytest import raises
from stack import Stack
from ex3 import reverse, PeopleChain, ShortChainError


###############################################################################
# Task 1: Stacks
###############################################################################
def test_reverse_many():
    """Test stack reverse on a large stack.

    Something fun to think about after this week's lab:
    how does the structure of this test remind you of queues?
    """
    stack = Stack()
    for i in range(100):
        stack.push(i)
    reverse(stack)
    for i in range(100):
        assert stack.pop() == i

    assert stack.is_empty()


def test_reverse_empty():
    """Test stack reverse on an empty stack."""
    stack = Stack()
    reverse(stack)
    assert stack.is_empty()


###############################################################################
# Task 2: A Chain of People
###############################################################################
def test_get_leader_simple():
    """Test get_leader (simple)."""
    chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
    assert chain.get_leader() == 'Iron Man'


def test_get_second_simple():
    """Test get_second (simple)."""
    chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
    assert chain.get_second() == 'Janna'


def test_get_third_simple():
    """Test get_third (simple)."""
    chain = PeopleChain(['Iron Man', 'Janna', 'Kevan'])
    assert chain.get_third() == 'Kevan'


@given(lists(text()), integers(min_value=1))
def test_get_nth_on_out_of_bounds_index(names: List[str], offset: int):
    """Test that get_nth raises a ShortChainError when given a too-large index.
    """
    chain = PeopleChain(names)

    # Use a with block and pytest's <raises> to assert that the following
    # code raises an error.
    with raises(ShortChainError):
        chain.get_nth(len(names) + offset)


if __name__ == '__main__':
    import pytest
    pytest.main()
