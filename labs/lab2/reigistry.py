"""Object-Oriented Programming: A system for organizing a 5K running race.

=== CSC148 Fall 2017 ===
Ousmane Amadou

=== Module description ===
This module contains two sample classes Tweet and Person that we developed
as way to introduce the major concepts of object-oriented programming.

Please note: this is a combined version for all students, so may contain
minor inconsistencies with what you saw during lecture.
"""

from enum import Enum      # Python library for expressing enumerated types
from typing import List    # Python library for expressing complex types

class Runner:
    """A runner participating in the 5k running race.

        === Attributes ===
        name: the name of the runner.
        e_mail: the email of the runner.
        s_cat: the speed category of the runner.
        withdrawn: whether racer has dropped out of the race.

        === Representation Invariants ===
        - s_cat is in [0, 1, 2, 3]
        - self.likes >= 0
    """
    # Attribute types
    name: str
    e_mail: str
    s_cat: int
    withdrawn: bool


    def __init__(self, name: str, e_mail: str, s_cat: int) -> None:
        """Initialize a new runner.

        """
        self.name = name
        self.e_mail = e_mail
        self.s_cat = s_cat
        self.withdrawn = False


    def withdraw(self) -> None:
        self.withdrawn = True



class Race:
    """A runner participating in the 5k running race.

        === Attributes ===
        runners: the runners participating in the race
        runners_sc: a dictionary whose keys are the speed categories, and whose
        value are a list of runners in a given speed category.

        === Representation Invariants ===
        - s_cat is in [0, 1, 2, 3]
        - self.likes >= 0
    """
    # Attribute types
    runners: List[Runner]
    runners_sc: {}

    def __init__(self) -> None:
        """Initializes new race.

        """
        self.runners = []
        self.runners_sc = {0:[],1:[],2:[],3:[]}

    def add_runner(self, runner: Runner) -> None:
        """Adds runner to race, and designated speed category.

        """
        self.runners.append(runner)
        self.runners_sc[runner.s_cat].append(runner)

    def get_runners_in_sc(self, cat: int) -> List[Runner]:
        """Returns runner in speed category <cat>

        """
        return self.runners_sc[cat]

    def get_runner_sc(self, runner: Runner) -> int:
        """Retruns speed category of runner. -1 if runner isn't in race
           or doesnt exist.

        """
        if runner in self.runners:
            return runner.s_cat
        return -1
