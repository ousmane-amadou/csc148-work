"""CSC148 Lab 5: Linked Lists

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===

This module runs timing experiments to determine how the time taken
to call len on a Python list vs a LinkedList grows as the list size grows.

To complete this code, you will again use the Timer class.  Here is a template
for how to use it with is_verbose set to False.

    with Timer('', is_verbose=False) as tm:
        # A block of code to be timed goes here.
        # The timer is "on" the whole time.

    # After the block ends, the attribute tm.interval stores the
    # total time taken to run the block of code.

Because is_verbose is set to False, the Timer will not printing anything
when the with-block is over.  This will be useful in our profile_len function,
which is not to print anything.  It leaves the client code---our main
block---in control of any output.

Because the Timer is set so as not to print anything, the string we pass to
it has no use.  So we might as well pass in the empty string.
"""
from typing import Tuple
from linked_list import LinkedList
from timer import Timer


def profile_len(list_size: int, n: int) -> Tuple[float, float]:
    """Return the average time taken (averaging over <n> repetitions) to
    call len on a Python list of length <list_size> and to call len on a
    LinkedList of length <list_size>.

    Do not print anything.
    """
    # Make both a Python list and a LinkedList of size <list_size>.
    lst = list(range(list_size))
    ll = LinkedList(lst)
    time1 = 0
    time2 = 0

    for i in range(n):
        with Timer('', is_verbose=False) as time:
            len(lst)
        time1 += time.interval
    time1 /= n

    for i in range(n):
        with Timer('', is_verbose=False) as time:
            len(ll)
        time2 += time.interval
    time2 /= n

    return time1, time2


if __name__ == '__main__':
    SIZES = [100, 1000, 10000, 100000]

    # For each size of list, profile len for a Python list vs. a LinkedList,
    # and print the results.
    for s in SIZES:
        results = profile_len(s, 1000)
        print('Size = {}, avg time for len(lst): {:.2e} and for len(ll): {:.2e}'
              .format(s, results[0], results[1]))
