"""CSC148 Exercise 7: Recursion Wrap-Up

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 7.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<http://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
from ex7 import anagrams


def test_empty_string():
    """Test anagrams on an empty string."""
    assert anagrams('', 1) == ['']


def test_one_letter():
    """Test anagrams on a single letter."""
    assert anagrams('a', 1) == ['a']


def test_dormitory():
    """Test anagrams on the string 'dormitory'."""
    assert anagrams('dormitory', 3) ==\
        ['dirty room', 'dormitory', 'room dirty']


def test_dormitory_with_limit():
    """Test anagrams on the string 'dormitory' with a smaller limit."""
    assert anagrams('dormitory', 1) == ['dirty room']


if __name__ == '__main__':
    import pytest
    pytest.main()
