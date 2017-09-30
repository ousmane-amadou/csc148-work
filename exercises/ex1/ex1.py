"""CSC148 Exercise 1: Basic Object-Oriented Programming

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for Exercise 1.
It contains two classes that work together:
- SuperDuperManager, which manages all the cars in the system
- Car, a class which represents a single car in the system

Your task is to design and implement the Car class, and then modify the
SuperDuperManager methods so that they make proper use of the Car class.

You may not modify the public interface of any of the SuperDuperManager methods.
We have marked the parts of the code you should change with TODOs, which you
should remove once you've completed them.

Notes:
  1. We'll talk more about private attributes on Friday's class.
     For now, treat them the same as any other instance attribute.
  2. You'll notice we use a trailing underscore for the parameter name
     "id_" in a few places. It is used to avoid conflicts with Python
     keywords. Here we want to have a parameter named "id", but that is
     already the name of a built-in function. So we call it "id_" instead.
"""
from typing import Dict, Optional, Tuple


class SuperDuperManager:
    """A class that keeps track of all cars in the Super Duper system.

    === Private Attributes ===
     _cars: A map of unique string identifiers to the corresponding Car.
     For example, _cars['car1'] would be a Car object corresponding to
     the id 'car1'.

    """
    _cars: Dict[str, 'Car']

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.

        There are no cars in the system when first created.
        """
        self._cars = {}

    @property
    def cars(self):
        """Give public access to _cars private attribute
        """
        return self._cars

    def add_car(self, id_: str, fuel: int) -> None:
        """Add a new car to the system.

        The new car is identified by a string <id_> , and has initial
        amount of fuel <fuel>.

        Do nothing if there is already a car with the <id_>.

        Precondition(s): fuel >= 0, len(id_) > 0

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car', 10)
        >>> 'cAr' in sp.cars.keys()
        False
        >>> sp.cars['car'].fuel
        10
        >>> sp = SuperDuperManager()
        >>> sp.add_car('boogadi', 10)
        >>> sp.add_car('roogadi', 15)
        >>> sp.cars['boogadi'].fuel
        10
        >>> sp.cars['roogadi'].fuel
        15
        """

        # Check to make sure the identifier isn't already used.
        if id_ not in self._cars:
            self._cars[id_] = Car(fuel)

    def move_car(self, id_: str, new_x: int, new_y: int) -> None:
        """Move the car with the given id.

        The car called <id_> should be moved to position (<new_x>, <new_y>).
        Do nothing if there is no car with the given id,
        or if the corresponding car does not have enough fuel.

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car', 5)
        >>> sp.move_car('car', 10, 20)
        >>> pos = (sp.cars['car'].x, sp.cars['car'].y)
        >>> pos
        (0, 0)

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car', 30)
        >>> sp.move_car('car', 10, 20)
        >>> pos = (sp.cars['car'].x, sp.cars['car'].y)
        >>> pos
        (10, 20)
        """
        if id_ in self._cars:
            dx = new_x - self._cars[id_].x
            dy = new_y - self._cars[id_].y

            # Check if car has enough fuel
            if self._cars[id_].fuel >= abs(dx) + abs(dy):
                self._cars[id_].move_horizontally(dx)
                self._cars[id_].move_vertically(dy)

    def get_car_position(self, id_: str) -> Optional[Tuple[int, int]]:
        """Return the position of the car with the given id.

        Return a tuple of the (x, y) position of the car with id <id_>.
        Return None if there is no car with the given id.

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car', 30)
        >>> sp.move_car('car', 10, 20)
        >>> sp.get_car_position('car')
        (10, 20)

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car', 0)
        >>> sp.move_car('car', 10, 20)
        >>> sp.get_car_position('car')
        (0, 0)
        """
        if id_ in self._cars:
            return (self._cars[id_].x, self._cars[id_].y)
        return None

    def get_car_fuel(self, id_: str) -> Optional[int]:
        """Return the amount of fuel of the car with the given id.

        Return None if there is no car with the given id.

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car', 30)
        >>> sp.move_car('car', 10, 20)
        >>> sp.get_car_fuel('car')
        0
        >>> sp.get_car_fuel('cAr')

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car', 20)
        >>> sp.get_car_fuel('car')
        20
        """
        if id_ in self._cars:
            return self._cars[id_].fuel
        return None

    def dispatch(self, x: int, y: int) -> None:
        """Move a car to the given location.

        Choose a car to move based on the following criteria:
        (1) Only consider cars that *can* move to the location.
            (Ignore ones that don't have enough fuel.)
        (2) After (1), choose the car that would move the *least* distance to
            get to the location.
        (3) If there is a tie in (2), pick the car whose id comes first
            alphabetically. Use < and/or > to compare the strings.
        (4) If no cars can move to the given location, do nothing.

        >>> sp = SuperDuperManager()
        >>> sp.add_car('car1', 100)
        >>> sp.add_car('Car1', 100)
        >>> sp.dispatch(50, 50)
        >>> sp.get_car_position('car1')
        (0, 0)
        >>> sp.get_car_position('Car1')
        (50, 50)
        >>> sp.add_car('car2', float('inf'))
        >>> sp.dispatch(float('inf'), float('inf'))
        >>> sp.get_car_position('car1')
        (0, 0)
        >>> sp.get_car_position('Car1')
        (50, 50)
        >>> sp.get_car_position('car2')
        (0, 0)
        """

        ctm_id = None         # ID of the car to move (the closest car)
        ctm_d = float('inf')  # Distance car to move must move to reach location

        for id_ in self._cars:
            d = abs(self._cars[id_].x - x) + abs(self._cars[id_].y - y)
            if d < ctm_d:
                ctm_id = id_
                ctm_d = d
            elif d == ctm_d:       # Covering case 3, as described in docstring
                if ctm_id is not None:
                    if id_ < ctm_id:
                        ctm_id = id_
                        ctm_d = d
                else:
                    ctm_id = id_
                    ctm_d = d

        if ctm_id is not None:
            self.move_car(ctm_id, x, y)


class Car:
    """A car in the Super system.

    === Private attributes ===
    _x: the x-coordinate of this car's position
    _y: the y-coordinate of this car's position
    _fuel: the amount of fuel remaining this car has remaining

    === Representation invariants ===
    _fuel >= 0
    """
    _x: int
    _y: int
    _fuel: int

    def __init__(self, fuel: int) -> None:
        """Initialize a new Super Duper car.

        """
        # All new cars start at position (0, 0)
        self._x = 0
        self._y = 0
        self._fuel = fuel

    @property
    def x(self):
        """Give public access to private variable _x """
        return self._x

    @property
    def y(self):
        """Give public access to private variable _y """
        return self._y

    @property
    def fuel(self):
        """Give public access to private variable _fuel """
        return self._fuel

    def move_horizontally(self, d: int) -> None:
        """Moves the car <d> units of distance horizontally, if there is at
        least <d> unit(s) of fuel availble. Otherwise, car doesn't move at all.

        >>> my_car = Car(10)
        >>> my_car.move_horizontally(10)
        >>> my_car.x
        10
        >>> my_car.y
        0
        >>> my_car.fuel
        0

        >>> my_car = Car(10)
        >>> my_car.move_horizontally(20)
        >>> my_car.x
        0
        >>> my_car.y
        0
        >>> my_car.fuel
        10
        """
        if self.fuel >= d:
            self._fuel -= abs(d)
            self._x += d

    def move_vertically(self, d: int) -> None:
        """Moves the car <d> units of distance vertically, if there is at
        least <d> unit(s) of fuel availble. Otherwise, car doesn't move at all.

        >>> my_car = Car(10)
        >>> my_car.move_vertically(10)
        >>> my_car.x
        0
        >>> my_car.y
        10
        >>> my_car.fuel
        0

        >>> my_car = Car(10)
        >>> my_car.move_vertically(20)
        >>> my_car.x
        0
        >>> my_car.y
        0
        >>> my_car.fuel
        10
        """
        if self.fuel >= d:
            self._fuel -= abs(d)
            self._y += d


if __name__ == '__main__':
    # Run python_ta to ensure this module passes all checks for
    # code inconsistencies and forbidden Python features.
    # Useful for debugging!

    import doctest
    doctest.testmod()
