"""Lab 11: Profiling sorting algorithms

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains code to perform timing experiments on various sorting
algorithms.
"""
import random
from typing import Callable

from timer import Timer
from sorting import mergesort


NUM_TRIALS = 100


def profile_alg(n: int, alg: Callable[[list], None]) -> None:
    """Run a timing experiment for sorting a list of length <n>."""
    total_time = 0
    for _ in range(NUM_TRIALS):
        lst = list(range(n))
        random.shuffle(lst)
        with Timer('', is_verbose=False) as t:
            alg(lst)

        total_time += t.interval

    print(f'{alg.__name__.ljust(10)} {n}: {total_time/NUM_TRIALS:<20}')


if __name__ == '__main__':
    SIZES = [1000, 2000, 4000, 8000]

    # Run the timing experiment on mergesort (non-mutating version)
    for size in SIZES:
        profile_alg(size, mergesort)

    # Run the timing experiment on mergesort2 (mutating version)
    # for size in SIZES:
    #     profile_alg(size, mergesort2)

    # Run the timing experiment on first version of timsort
    # for size in SIZES:
    #     profile_alg(size, timsort)

    # Run the timing experiment on second version of timsort
    # for size in SIZES:
    #     profile_alg(size, timsort2)

    # Run the timing experiment on the built-in list.sort
    for size in SIZES:
        profile_alg(size, list.sort)
