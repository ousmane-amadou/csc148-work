"""Assignment 1 - Simulation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Simulation class, which is the main class for the
bike-share simulation.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'

# Useful Constants
S = 'start'
E = 'end'
TLA = 'time_low_availability'
TLU = 'time_low_unoccupied'

M = {
    'start': 'max_start',
    'end': 'max_end',
    'time_low_availability': 'max_time_low_availability',
    'time_low_unoccupied': 'max_time_low_unoccupied'
}


class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    active_rides:
        A list of all rides currently active in the simulation
    all_stations:
        A dictionary containing all the stations in this simulation.
    ride_queue:
        A priority queue containing all ride events in order of most recently
        occurring ride events, to least recently occurring ride events
    visualizer:
        A helper class for visualizing the simulation.

    === Representation invariants ==
    active_rides[i].start.time >= current time
    """
    all_stations: Dict[str, 'Station']
    all_rides: List[Ride]
    active_rides: List[Ride]
    visualizer: Visualizer
    ride_queue: PriorityQueue

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.visualizer = Visualizer()
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self.ride_queue = PriorityQueue()

    def update_statistics(self):
        """Updates the statistics of every station. """
        for st_id in self.all_stations:
            station = self.all_stations[st_id]
            station.update_statistics()

    def init_ride_queue(self, start: datetime):
        """Initializes the ride_queue with RideStartEvents starting at or
        after <start> time
        """
        for ride in self.all_rides:
            if ride.start_time >= start:
                self.ride_queue.add(RideStartEvent(self, ride))

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        step = timedelta(minutes=1)  # Each iteration spans one minute of time

        st_to_draw = list(self.all_stations.values())
        current = start  # Sets current time to simulation start time

        # Adds all rides that start after start time to ride_queue
        self.init_ride_queue(start)

        # Simulation Loop (halt when current time exceeds end time)
        while current < end:
            self._update_active_rides_fast(current)
            self.update_statistics()
            self.visualizer.render_drawables(st_to_draw+self.active_rides,
                                             current)

            current += step

        # Leave this code at the very bottom of this method.
        # It will keep the visualization window open until you close
        # it by pressing the 'X'.
        while True:
            if self.visualizer.handle_window_events():
                return  # Stop the simulation

    def _update_active_rides(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.
        """

        for ride in self.all_rides:
            prev_active = ride in self.active_rides
            curr_active = (time >= ride.start_time) and (time <= ride.end_time)

            if prev_active and not curr_active:
                ride.end.update_state('end')
                self.active_rides.remove(ride)
            elif not prev_active and curr_active:
                ride.start.update_state('start')
                self.active_rides.append(ride)

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
        """

        stats = {
            'max_start': ('', -1),
            'max_end': ('', -1),
            'max_time_low_availability': ('', -1),
            'max_time_low_unoccupied': ('', -1)
        }

        for st_id in self.all_stations:
            st_stats = self.all_stations[st_id].stats
            st_name = self.all_stations[st_id].name

            if stats[M[S]][1] < st_stats[S]:
                stats[M[S]] = (st_name, st_stats[S])
            elif (stats[M[S]][1] == st_stats[S]) and (st_name < stats[M[S]][0]):
                stats[M[S]] = (st_name, st_stats[S])

            if stats[M[E]][1] < st_stats[E]:
                stats[M[E]] = (st_name, st_stats[E])
            elif (stats[M[E]][1] == st_stats[E]) and (st_name < stats[M[E]][0]):
                stats[M[E]] = (st_name, st_stats[E])

            if stats[M[TLA]][1] < st_stats[TLA]:
                stats[M[TLA]] = (st_name, st_stats[TLA])
            elif (stats[M[TLA]][1] == st_stats[TLA]) and (st_name < stats[M[TLA]][0]):
                stats[M[TLA]] = (st_name, st_stats[TLA])

            if stats[M[TLU]][1] < st_stats[TLU]:
                stats[M[TLU]] = (st_name, st_stats[TLU])
            elif (stats[M[TLU]][1] == st_stats[TLU]) and (st_name < stats[M[TLU]][0]):
                stats[M[TLU]] = (st_name, st_stats[TLU])

        return stats

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.
        """

        while not self.ride_queue.is_empty():
            ride_event = self.ride_queue.remove()

            # Process event if it occurs during/before current time,
            # Otherwise add event back to ride_queue to be processed at
            # a future time
            if Event(self, time) < ride_event:
                self.ride_queue.add(ride_event)
                return
            else:
                spawned_events = ride_event.process()
                for event in spawned_events:
                    self.ride_queue.add(event)


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* create_rides() because the
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
        st_id = s['n']
        name = s['s']
        location = (float(s['lo']), float(s['la']))
        bike_count = int(s['da'])
        capcity = int(s['ba']) + bike_count

        stations[st_id] = Station(location, capcity, bike_count, name)
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
            try:
                start_time = datetime.strptime(line[0], DATETIME_FORMAT)
                start_station = stations[line[1]]

                end_time = datetime.strptime(line[2], DATETIME_FORMAT)
                end_station = stations[line[3]]
                rides.append(Ride(start_station, end_station,
                                  (start_time, end_time)))
            except KeyError:
                pass

    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.

    === Attributes ===
    simulation:
        the simulation instancce in which the event occurs
    time:
        the time stamp of the event
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
    """An event corresponding to the start of a ride.

    === Attributes ===
    ride:
        The ride that triggers this RideStartEvent instance.

    === Representation Invariants ===
    self.time == self.ride.start_time
    """
    ride: Ride

    def __init__(self, simulation: 'Simulation', ride: Ride) -> None:
        """Initialize a new RideStartEvent."""
        Event.__init__(self, simulation, ride.start_time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.

        Note: The list of new events in this particular case should be a
        list containing a single RideEndEvent that corresponds with
        the end time of self.ride.
        """
        self.ride.start.update_state('start')
        self.simulation.active_rides.append(self.ride)

        return [RideEndEvent(self.simulation, self.ride)]


class RideEndEvent(Event):
    """An event corresponding to the end of a ride.

    === Attributes ===
    ride:
        The ride that triggers this RideEndEvent instance.

    === Representation Invariants ===
    self.time == self.ride.end_time
    """
    ride: Ride

    def __init__(self, simulation: 'Simulation', ride: Ride) -> None:
        """Initialize a new RideEndEvent."""
        Event.__init__(self, simulation, ride.end_time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        Note: This should be an empty list, since there is no case in
        which a RideEndEvent should spawn new events.
        """
        self.ride.end.update_state('end')
        self.simulation.active_rides.remove(self.ride)
        return []


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 0, 0),
            datetime(2017, 6, 1, 9, 0, 0))
    return sim.calculate_statistics()


if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['create_stations', 'create_rides'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'csv', 'datetime', 'json',
            'bikeshare', 'container', 'visualizer'
        ]
    })
    print(sample_simulation())
