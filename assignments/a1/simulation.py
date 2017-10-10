"""Assignment 1 - Simulation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Simulation class, which is the main class for your
bike-share simulation.

At the bottom of the file, there is a sample_simulation function that you
can use to try running the simulation at any time.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

import pygame
# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    active_rides:
        TODO
    all_stations:
        A dictionary containing all the stations in this simulation.
    visualizer:
        A helper class for visualizing the simulation.
    """
    all_stations: Dict[str, 'Station']
    all_rides: List[Ride]
    active_rides: List[Ride]
    visualizer: Visualizer
    ride_handler: PriorityQueue

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.visualizer = Visualizer()
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self.ride_handler = PriorityQueue()

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        step = timedelta(minutes=1)  # Each iteration spans one minute of time

        st_to_draw = list(self.all_stations.values())    # Stations that need to be rendered
        current = start                                  # Sets current time to simulation start time

        for ride in self.all_rides:                      # Adds all rides to PriorityQueue
            self.ride_handler.add(RideStartEvent(self, ride))


        # Simulation Loop (halt when current time exceeds end time)
        while current < end:
            self._update_active_rides(current)        # Changes rides_to_draw by side effect
            self.visualizer.render_drawables(st_to_draw+self.active_rides, current)

            current += step

        # Leave this code at the very bottom of this method.
        # It will keep the visualization window open until you close
        # it by pressing the 'X'.
        while True:
            pygame.event.peek()
            #if self.visualizer.handle_window_events():
            #    return  # Stop the simulation

    def _update_active_rides(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   Loop through `self.all_rides` and compare each Ride's start and
            end times with <time>.

            If <time> is between the ride's start and end times (inclusive),
            then add the ride to self.active_rides if it isn't already in
            that list.

            Otherwise, remove the ride from self.active_rides if it is in
            that list.

        -   This means that if a ride started before the simulation's time
            period but ends during or after the simulation's time period,
            it should still be added to self.active_rides.

            NOTES:
                * Need to find a way to find number of bikes currently at station
                * Need to find a way to limit number of bikes getting into station
        """

        for ride in self.all_rides:
            prev_active = ride in self.active_rides
            curr_active = (time >= ride.start_time) and (time <= ride.end_time)

            if prev_active and not curr_active:  # Indicates a ride that has just ended
                ride.end.update_state('end')         # Should remove bike from station, and update stats
                self.active_rides.remove(ride)
            elif not prev_active and curr_active:  # Indicates a ride that has just been started
                ride.start.update_state('start')         # Should add bike to station, and update stats
                self.active_rides.append(ride)
            else:
                ride.end.update_state('unchanged')  # Just update statistics


    def calculate_statistics(self) -> Dict[str, Tuple[str, float]]:
        """Return a dictionary containing statistics for this simulation.

        The returned dictionary has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'max_start'
          - 'max_end'
          - 'max_time_low_availability'
          - 'max_time_low_unoccupied'

        The corresponding value of each key is a tuple of two elements,
        where the first element is the name (NOT id) of the station that has
        the maximum value of the quantity specified by that key,
        and the second element is the value of that quantity.

        For example, the value corresponding to key 'max_start' should be the
        name of the station with the most number of rides started at that
        station, and the number of rides that started at that station.

        NOTES:
            What about cases where two stations tie?
        """
        stats = {
            'max_start': ('', -1),
            'max_end': ('', -1),
            'max_time_low_availability': ('', -1),
            'max_time_low_unoccupied': ('', -1)
        }

        for st_id in self.all_stations:
            st_stats = self.all_stations[st_id].stats
            if stats['max_start'][1] > st_stats['start']:
                stats['max_start'] = (st_id, st_stats['start'])
            if stats['max_end'][1] > st_stats['end']:
                stats['max_end'] = (st_id, st_stats['end'])
            if stats['max_time_low_availability'][1] > st_stats['time_low_availability']:
                stats['max_time_low_availability'] = (st_id, st_stats['time_low_availability'])
            if stats['max_time_low_occupancy'][1] > st_stats['time_low_occupancy']:
                stats['max_time_low_occupancy'] = (st_id, st_stats['time_low_occupancy'])

        return stats

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   see Task 5 of the assignment handout
        """

        while not self.ride_handler.is_empty():
            rideEvent = self.ride_handler.remove()

            if Event(self, time) < rideEvent:     # if top priority event comes after current time
                self.ride_handler.add(rideEvent)
                return
            else:                                 # if top priority event comes before or during curr time
                rideEvent.process()


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Each key in the returned dictionary is a station id,
    and each value is the corresponding Station object.
    Note that you need to call Station(...) to create these objects!

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* _read_rides because the
    rides CSV file refers to station ids.

    >>> stations = create_stations('stations.json')
    >>> test_id = '6023'
    >>> test_id in stations
    True
    """
    # Read in raw data using the json library.
    with open(stations_file) as file:
        raw_stations = json.load(file)

    stations = {}
    for s in raw_stations['stations']:
        # Extract the relevant fields from the raw station JSON.
        # s is a dictionary with the keys 'n', 's', 'la', 'lo', 'da', and 'ba'
        # as described in the assignment handout.
        # NOTE: all of the corresponding values are strings, and so you need
        # to convert some of them to numbers explicitly using int() or float().
        id = s['n']
        name = s['s']
        location = (float(s['lo']), float(s['la']))
        bike_count = int(s['da'])
        capcity = int(s['ba']) + bike_count

        stations[id] = Station(location, capcity, bike_count, name)
    return stations


def create_rides(rides_file: str,
                 stations: Dict[str, 'Station']) -> List['Ride']:
    """Return the rides described in the given CSV file.

    Lookup the station ids contained in the rides file in <stations>
    to access the corresponding Station objects.

    Ignore any ride whose start or end station is not present in <stations>.

    Precondition: rides_file matches the format specified in the
                  assignment handout.
    """
    rides = []

    with open(rides_file) as file:
        for line in csv.reader(file):
            # line is a list of strings, following the format described
            # in the assignment handout.
            #
            # Convert between a string and a datetime object
            # using the function datetime.strptime and the DATETIME_FORMAT
            # constant we defined above. Example:
            # >>> datetime.strptime('2017-06-01 8:00', DATETIME_FORMAT)
            # datetime.datetime(2017, 6, 1, 8, 0)

            try:
                start_time = datetime.strptime(line[0], DATETIME_FORMAT)
                start_station = stations[line[1]]

                end_time = datetime.strptime(line[2], DATETIME_FORMAT)
                end_station = stations[line[3]]
                rides.append(Ride(start_station, end_station, (start_time, end_time)))
            except KeyError:
                pass

    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.
    """
    simulation: 'Simulation'
    time: datetime

    def __init__(self, simulation: 'Simulation', time: datetime) -> None:
        """Initialize a new event."""
        self.simulation = simulation
        self.time = time

    def __lt__(self, other: 'Event') -> bool:
        """Return whether this event is less than <other>.

        Events are ordered by their timestamp.
        """
        return self.time < other.time

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        raise NotImplementedError


class RideStartEvent(Event):
    """An event corresponding to the start of a ride."""
    ride: Ride

    def __init__(self, simulation: 'Simulation', ride: Ride) -> None:
        """Initialize a new event."""
        Event.__init__(self, simulation, ride.start_time)

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        self.ride.update_state('start')
        return [RideEndEvent(self.simulation, self.ride)]


class RideEndEvent(Event):
    """An event corresponding to the start of a ride."""
    ride: Ride

    def __init__(self, simulation: 'Simulation', ride: Ride) -> None:
        """Initialize a new event."""
        Event.__init__(self, simulation, ride.end_time)

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        self.ride.update_state('end')
        return []

def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 0, 0),
            datetime(2017, 6, 1, 9, 0, 0))
    return sim.calculate_statistics()


if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-io': ['create_stations', 'create_rides'],
    #     'allowed-import-modules': [
    #         'doctest', 'python_ta', 'typing',
    #         'csv', 'datetime', 'json',
    #         'bikeshare', 'container', 'visualizer'
    #     ]
    # })
    print(sample_simulation())
