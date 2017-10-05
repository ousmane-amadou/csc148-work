"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===

This module runs timing experiments to determine how the time taken
to enqueue or dequeue grows as the queue size grows.

To complete this code, you will use the Timer class.  Here is a template
for how to use it.

Read through the docstring of the Timer class to understand how to use it.
"""
from myqueue import Queue
from timer import Timer
import matplotlib.pyplot as plt


def _profile_enqueue(queue_size: int, n: int) -> None:
    """Report the time taken to perform enqueue operations.

    Specifically, report the time taken to perform a single Queue.enqueue
    operation on <n> queues, each of size <queue_size>.
    (We do this on multiple queues to slow down the trials a little.)
    """
    queue_list = []
    for i in range(n):
        new_queue = Queue()
        new_queue._items = list(range(queue_size))
        queue_list.append(new_queue)

    with Timer('enqueue') as my_timer:
        for new_queue in queue_list:
            new_queue.enqueue(10)

    # TODO: implement this function by following the steps in the comments.
    # Experiment preparation: make a list containing <n> queues,
    # each of size <queue_size>. The elements you enqueue don't matter.
    # You can "cheat" here and set your queue's _items attribute
    # directly to a list of the appropriate size by writing something like
    #
    # queue._items = list(range(queue_size))
    #
    # to save a bit of time in setting up the experiment.

    # First, make a list containing <n> queues of size <queue_size>.

    # Second, for each of the <n> queues, enqueue a single item.
    # (Wrap the code in a Timer block to measure the total time taken.)


def _profile_dequeue(queue_size: int, n: int) -> float:
    """Report the time taken to perform enqueue operations.

    Specifically, report the time taken to perform a single Queue.enqueue
    operation on <n> queues, each of size <queue_size>.
    (We do this on multiple queues to slow down the trials a little.)
    """
    # TODO: implement this function in a similar way to _profile_enqueue.
    # Experiment preparation: make a list containing <n> queues,
    # each of size <queue_size>.
    # You can "cheat" here and set your queue's _items attribute
    # directly to a list of the appropriate size by writing something like
    #
    #
    #
    # to save a bit of time in setting up the experiment.

    queue_list = []
    for i in range(n):
        new_queue = Queue()
        new_queue._items = list(range(queue_size))
        queue_list.append(new_queue)

    with Timer('dequeue') as my_timer:
        for new_queue in queue_list:
            new_queue.dequeue()

    return my_timer.interval

def time_queue() -> None:
    """Profile enqueue and dequeue on various queue sizes."""
    # The different parameters for our timing runs.
    # Feel free to adjust this a little if it runs very slowly
    # on your computers.
    sizes = [10000, 20000, 40000, 80000, 160000]
    trials = 300

    y = []
    for size in sizes:
        _profile_enqueue(size, trials)
        _profile_dequeue(size, trials)

    # TODO: Run _profile_enqueue and _profile_enqueue with the different
    # experiment parameters (sizes and trials).


if __name__ == '__main__':
    time_queue()
