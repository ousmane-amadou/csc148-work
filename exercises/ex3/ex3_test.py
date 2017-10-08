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
from hypothesis import given, assume
from hypothesis.strategies import lists, text, integers
from pytest import raises
from stack import Stack
from ex3 import reverse, PeopleChain, ShortChainError, merge_alternating


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

@given(integers(min_value=0, max_value=100))
def test_merge_alternating(stack_size: int):
    stack1 = Stack()
    stack2 = Stack()
    i = 0
    while i < stack_size:
        stack1.push(i)
        stack2.push(stack_size+i)
        i += 1

    stack = merge_alternating(stack1, stack2)
    while not stack.is_empty():
        assert stack.pop() == stack1.pop()
        assert stack.pop() == stack2.pop()

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

@given(lists(text()), integers(min_value=1))
def test_get_nth(names: List[str], n: int):
    """Test that get_nth raises a ShortChainError when given a too-large index.
    """
    assume(n <= len(names))
    chain = PeopleChain(names)
    assert names[n-1] == chain.get_nth(n)


if __name__ == '__main__':
    import pytest
    pytest.main()
