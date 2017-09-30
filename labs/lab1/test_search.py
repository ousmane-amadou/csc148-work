"""CSC148 Lab 1

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module illustrates a simple unit test for our binary_search function.
"""
from search import binary_search


def test_search():
    """Simple test for binary_search."""
    assert binary_search([0, 5, 10, 15, 20, 25, 30, 35, 40], 5) == 1


if __name__ == '__main__':
    import pytest
    pytest.main()
