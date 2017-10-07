"""Assignment 1 - Bike-share objects

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Station and Ride classes, which store the data for the
objects in this simulation.

There is also an abstract Drawable class that is the superclass for both
Station and Ride. It enables the simulation to visualize these objects in
a graphical window.
"""
from datetime import datetime
from typing import Dict, Tuple


# Sprite files
STATION_SPRITE = 'stationsprite.png'
RIDE_SPRITE = 'bikesprite.png'


class Drawable:
    """A base class for objects that the graphical renderer can be drawn.

    === Public Attributes ===
    sprite:
        The filename of the image to be drawn for this object.
    """
    sprite: str

    def __init__(self, sprite_file: str) -> None:
        """Initialize this drawable object with the given sprite file.
        """
        self.sprite = sprite_file

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in long/lat coordinates
        **UPDATED**: make sure the first coordinate is the longitude,
        and the second coordinate is the latitude.
    name: str
        name of the station
    num_bikes: int
        current number of bikes at the station

    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    """
    # Private Attributes

    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    stats: Dict['str', int]


    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        Drawable.__init__(self, STATION_SPRITE)
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name

        self.stats = {
            'start': 0,
            'end': 0,
            'time_low_availability': 0,
            'time_low_unoccupied': 0
        }

    def update_state(self, event: str) -> None:
        """ Update the current state of station.
        Also updates certain stastistics.
        """
        if event == 'start':
            self.stats['start'] +=1
            self.num_bikes -= 1     # Make sure num_bikes > 0
        elif event == 'end':
            self.stats['end'] +=1
            self.num_bikes += 1    # Make sure num_bikes <= capacity

        if self.num_bikes <= 5:
            self.stats['time_low_availability'] += 1

        if (self.capacity - self.num_bikes) >= 5:
            self.stats['time_low_occupancy'] += 1

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return self.location


class Ride(Drawable):
    """A ride using a Bixi bike.

    === Attributes ===
    start:
        the station where this ride starts
    end:
        the station where this ride ends
    start_time:
        the time this ride starts
    end_time:
        the time this ride ends

    === Representation Invariants ===
    - start_time < end_time
    """
    start: Station
    end: Station
    start_time: datetime
    end_time: datetime

    def __init__(self, start: Station, end: Station,
                 times: Tuple[datetime, datetime]) -> None:
        """Initialize a ride object with the given start and end information.
        """
        Drawable.__init__(self, RIDE_SPRITE)
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        # Calculate the total time of ride from start station to end station
        ride_time = (self.end_time - self.start_time).total_seconds()

        # Calculuate the speed ride goes in the logitudinal direction
        dx = self.start.get_position(time)[0] - self.end.get_position(time)[0]
        sp_x = dx / ride_time.total_seconds()

        # Calculuate the speed ride goes in the latitudinal direction
        dy = self.start.get_position(time)[1] - self.end.get_position(time)[1]
        sp_y = dy / ride_time.total_seconds()

        return (self.start.get_position(time)[0] + sp_x*ride_time,
                       self.start.get_position(time)[1] + sp_y*ride_time)




if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
