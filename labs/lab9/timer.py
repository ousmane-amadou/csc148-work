"""CSC148 Basic Timing Tool

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains a Timer class which can be used to measure the time
taken when executing a block of Python code.

Timer is used as a context manager; run help(Timer) to see example usage
for this class.

For more resources to learn about time profiling in Python, check out
https://docs.python.org/3.6/library/profile.html.
"""
import time
from typing import Optional


class Timer:
    """A Python context manager used to measure and output the amount of time
    a block of code takes.

    === Basic Usage ===

    Put the code to be timed inside a "with" block, and call the Timer
    constructor with a descriptive label for that code block.

    The code will be executed, and the amount of time taken will be printed.

    >>> with Timer('sum ints'):
    ...     sum = 0
    ...     for i in range(1000):
    ...         sum += 1
    sum ints took 0.00015279301442205906 seconds

    If you want to access the amount of time the block took as a Python value,
    use an "as" clause to give the Timer object a name.  It will have an
    attribute called <interval> that records the time taken.

    >>> with Timer('sum ints') as my_timer:
    ...     sum = 0
    ...     for i in range(1000):
    ...         sum += 1
    sum ints took 0.00015279301442205906 seconds
    >>> my_timer.interval
    0.00015279301442205906

    === Attributes ===
    label:
        A label to describe the block of code.
    interval:
        The amount of time the block took, or None when the block is first
        created.
    """
    label: str
    interval: Optional[float]

    # === Private Attributes ===
    _start: Optional[float]
    _end: Optional[float]
    _is_verbose: bool

    def __init__(self,
                 label: str = 'Your code',
                 is_verbose: bool = True) -> None:
        """Initialize a Timer.

        <label> describes the block of code.
        """
        self.label = label
        self._is_verbose = is_verbose
        self.interval = None
        self.start = None
        self.end = None

    def __enter__(self) -> 'Timer':
        """Enter a timed context."""
        self.start = time.perf_counter()
        return self

    # The parameters have more specific types than object, but for simplicity,
    # we are declaring them as objects.
    def __exit__(self, exc_type: object, exc_value: object,
                 exc_trace: object) -> bool:
        """Exit a timed context."""
        self.end = time.perf_counter()
        self.interval = self.end - self.start
        if self._is_verbose:
            print('{label} took {time} seconds'.format(label=self.label,
                                                       time=self.interval))

        return False
