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
    name:
        name of the station
    num_bikes:
        current number of bikes at the station
    stats:
        Has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'start'
          - 'end'
          - 'time_low_availability'
          - 'time_low_unoccupied'

    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    - stats[key] >= 0
    """
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
        """ Update the current 'state' of the station after a ride <event> event
        occurs at this station during the simulation.

        Note: The state of a station includes all values of its attributes
        excluding name and location, since those values remain constant.
        """
        # Update attributes in accordance with <event>
        if event == 'start' and self.num_bikes > 0:
            self.stats['start'] += 1
            self.num_bikes -= 1
        elif event == 'end' and self.num_bikes < self.capacity:
            self.stats['end'] += 1
            self.num_bikes += 1

    def update_statistics(self):
        """ Update statistics as specified in Assignment description.
        Note: We add 60 seconds, rather than 1 minute
        """
        if self.num_bikes <= 5:
            self.stats['time_low_availability'] += 60

        if (self.capacity - self.num_bikes) <= 5:
            self.stats['time_low_unoccupied'] += 60

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.
        Note that the station's location does *not* change over time.
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
    - start_time - end_time >= timedelta(minutes = 1)
      (that is the shortest possible time of a ride is 1 minute)
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
        Precondition: self.start_time <= time <= self.end_time
        """

        if time == self.start_time:
            return (self.start.get_position(time)[0],
                    self.start.get_position(time)[1])
        elif time == self.end_time:
            return (self.end.get_position(time)[0],
                    self.end.get_position(time)[1])

        # Calculate the total time of ride from start station to end station
        total_ride_time = (self.end_time - self.start_time).total_seconds()
        ride_time = (time - self.start_time).total_seconds()

        # Calculuate the speed ride goes in the logitudinal direction
        dx = self.end.get_position(time)[0] - self.start.get_position(time)[0]
        sp_x = dx / total_ride_time

        # Calculuate the speed ride goes in the latitudinal direction
        dy = self.end.get_position(time)[1] - self.start.get_position(time)[1]
        sp_y = dy / total_ride_time

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
