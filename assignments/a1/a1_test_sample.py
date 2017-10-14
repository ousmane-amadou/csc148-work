"""CSC148 Assignment 1: Sample tests

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 1.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<http://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
from datetime import datetime, timedelta
from math import isnan
import os
import pygame
import json
from pytest import approx
from bikeshare import Ride, Station
from hypothesis import given, assume
from hypothesis.strategies import integers, floats, tuples
from simulation import Simulation, create_stations, create_rides


###############################################################################
# Sample tests for Task 1
###############################################################################
def test_create_stations_simple():
    """Test reading in a station from provided sample stations.json.
    """
    stations = create_stations('stations.json')
    test_id = '6023'
    assert test_id in stations

    station = stations[test_id]
    assert isinstance(station, Station)
    assert station.name == 'de la Commune / Berri'
    assert station.location == (-73.54983, 45.51086)  # NOTE: (long, lat) coordinates!
    assert station.num_bikes == 18
    assert station.capacity == 39

def test_create_stations():
    """Test reading in a station from provided sample stations.json.
    """
    stations = create_stations('stations.json')

    with open('stations.json') as file:
        raw_stations = json.load(file)

    for s in raw_stations['stations']:
        id = s['n']
        name = s['s']
        location = (float(s['lo']), float(s['la']))
        bike_count = int(s['da'])
        capcity = int(s['ba']) + bike_count

        assert stations[id].name == name
        assert stations[id].location == location
        assert stations[id].num_bikes == bike_count
        assert stations[id].capacity == capcity

        assert isinstance(stations[id], Station)

def test_create_rides_simple():
    """Test reading in a rides file from provided sample sample_rides.csv.

    NOTE: This test relies on test_create_stations working correctly.
    """
    stations = create_stations('stations.json')
    rides = create_rides('sample_rides.csv', stations)

    # Check the first ride
    ride = rides[0]
    assert isinstance(ride, Ride)
    assert ride.start is stations['6134']
    assert ride.end is stations['6721']
    assert ride.start_time == datetime(2017, 6, 1, 7, 31, 0)
    assert ride.end_time == datetime(2017, 6, 1, 7, 54, 0)


###############################################################################
# Sample tests for Task 2
###############################################################################
def test_get_position_station():
    """Test get_position for a simple station.
    """
    stations = create_stations('stations.json')
    test_id = '6023'
    assert test_id in stations

    station = stations[test_id]
    time = datetime(2017, 9, 1, 0, 0, 0)  # Note: the time shouldn't matter.
    assert station.get_position(time) == (-73.54983, 45.51086)

@given(integers(min_value=1, max_value=10**1), tuples(floats(max_value=10**1), floats(max_value=10**1)),
       tuples(floats(max_value=10 ** 1), floats(max_value=10 ** 1)))
def test_get_position_ride(ride_time, station_start_location, station_end_location):
    """Test get_position for a simple ride.
    """
    assume(not isnan(station_start_location[0]))
    assume(not abs(station_start_location[0]) == float('Inf'))

    assume(not isnan(station_start_location[1]))
    assume(not abs(station_start_location[1]) == float('Inf'))

    assume(not isnan(station_end_location[0]))
    assume(not abs(station_end_location[0]) == float('Inf'))

    assume(not isnan(station_end_location[1]))
    assume(not abs(station_end_location[1]) == float('Inf'))

    # 1. Generate random stations
    station_start = Station(station_start_location, cap=10, num_bikes=10, name="generated")
    station_end = Station(station_end_location, cap=10, num_bikes=10, name="generated")

    # 2. Generate Random end time from a fixed start time
    start_time = datetime(2017, 9, 1, 0, 0, 0)
    end_time = start_time + timedelta(minutes=ride_time)

    ride = Ride(station_start, station_end, (start_time, end_time))

    # Check ride endpoints. We use pytest's approx function to
    # avoid floating point issues.
    assert ride.get_position(ride.start_time) == approx(ride.start.location)
    assert ride.get_position(ride.end_time) == approx(ride.end.location)

    # Check ride at specific time
    current_time = start_time
    total_displacement = (station_end_location[0] - station_start_location[0],
                          station_end_location[1] - station_start_location[1])
    while current_time < end_time:
        coeff = (current_time-start_time).total_seconds() / (end_time-start_time).total_seconds()
        current_location = (station_start_location[0] + coeff*total_displacement[0],
                            station_start_location[1] + coeff*total_displacement[1])

        assert ride.get_position(current_time) == approx(current_location)
        current_time += timedelta(minutes=1)



###############################################################################
# Sample tests for Task 4
###############################################################################
def test_statistics_simple():
    """A very small test simulation.

    This runs a simulation on the sample data files
    in the time range 9:30 to 9:45, in which there's only
    one ride (the very last ride in the file).
    """
    os.environ['SDL_VIDEODRIVER'] = 'dummy'                 # Ignore this line
    sim = Simulation('stations.json', 'sample_rides.csv')
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))  # Ignore this line

    sim.run(datetime(2017, 6, 1, 9, 30, 0),
            datetime(2017, 6, 1, 9, 45, 0))
    stats = sim.calculate_statistics()

    # Only one ride started!
    assert stats['max_start'] == (
        sim.all_stations['6091'].name,
        1
    )

    # Only one ride ended!
    assert stats['max_end'] == (
        sim.all_stations['6052'].name,
        1
    )

    # Many stations spent all 15 minutes (900 seconds) with
    # "low availability" or "low unoccupied".
    # We pick the ones whose names are *smallest* when compared
    # using <. Note that numbers come before letters in this ordering.

    # This station starts with only 3 bikes at the station.
    assert stats['max_time_low_availability'] == (
        '15e avenue / Masson',
        900  # 900 seconds
    )

    # This stations starts with only 1 unoccupied spot.
    assert stats['max_time_low_unoccupied'] == (
        '10e Avenue / Rosemont',
        900  # 900 seconds
    )

## More Tests
def test_ride_ends_outside_run():
    """Test a special case: when a ride ends outside the run period.
    """
    os.environ['SDL_VIDEODRIVER'] = 'dummy'                 # Ignore this line
    sim = Simulation('stations.json', 'sample_rides.csv')
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))  # Ignore this line

    # This last ride in the sample_rides.csv file now begins
    # during the simulation run, but ends after the run.
    sim.run(datetime(2017, 6, 1, 9, 30, 0),
            datetime(2017, 6, 1, 9, 40, 0))
    stats = sim.calculate_statistics()

    # One ride still started.
    assert stats['max_start'] == (
        sim.all_stations['6091'].name,
        1
    )

    # *No* rides were ended during the simulation time period.
    # As in the previous test, we pick the station whose name
    # is smallest when compared with <.
    assert stats['max_end'] == (
        '10e Avenue / Rosemont',
        0
    )


if __name__ == '__main__':
    import pytest
    pytest.main(['a1_test_sample.py'])
