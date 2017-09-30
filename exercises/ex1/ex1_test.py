"""CSC148 Exercise 1: Basic Object-Oriented Programming

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 1.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on testing, please review the Week 1 lecture notes on
the course website.

Note: this file is for support purposes only, and is not part of your submission.
"""
from hypothesis import given
from hypothesis.strategies import integers, text

from ex1 import SuperDuperManager


def test_move_simple():
    """Test moving a car to another location."""
    manager = SuperDuperManager()
    manager.add_car('car1', 2)
    manager.add_car('car2', 10)
    manager.add_car('car3', 20)
    manager.move_car('car2', 2, 3)
    assert manager.get_car_position('car2') == (2, 3)
    assert manager.get_car_fuel('car2') == 5


def test_move_not_enough():
    """Test moving a car that doesn't have enough fuel."""
    manager = SuperDuperManager()
    manager.add_car('car1', 2)
    manager.add_car('car2', 10)
    manager.add_car('car3', 20)
    manager.move_car('car2', 2, 3)
    manager.move_car('car1', 3, 5)
    assert manager.get_car_position('car1') == (0, 0)
    assert manager.get_car_fuel('car1') == 2


def test_move_negative():
    """Test moving a car to a position with negative coordinates."""
    manager = SuperDuperManager()
    manager.add_car('car1', 2)
    manager.add_car('car2', 10)
    manager.add_car('car3', 20)
    manager.move_car('car2', 2, 3)
    manager.move_car('car3', -2, -3)
    assert manager.get_car_position('car3') == (-2, -3)
    assert manager.get_car_fuel('car3') == 15



@given(text(), integers(min_value=0))
def test_add_car_returns_none(id_, fuel):
    """Check that add_car always returns None."""
    manager = SuperDuperManager()
    assert manager.add_car(id_, fuel) is None


@given(text(), integers(min_value=0))
def test_car_initial_fuel(id_, fuel):
    """Check that a car's initial fuel is set properly.
    """
    manager = SuperDuperManager()
    manager.add_car(id_, fuel)
    assert fuel == manager.get_car_fuel(id_)


@given(text(), integers(min_value=0))
def test_car_initial_position(id_, fuel):
    manager = SuperDuperManager()
    manager.add_car(id_, fuel)
    assert (0, 0) == manager.get_car_position(id_)


if __name__ == '__main__':
    import pytest
    pytest.main()
