import unittest

from webapp import App

class Planet:
    def __init__(self, id, name, distance, flights):
        self._flights = flights
        self.distance = distance
        self.name = name
        self.id = id

    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance

    def get_flight_count(self):
        return len(self._flights)

    def flights(self):
        return self._flights

class Flight:
    def __init__(self, id, date):
        self._date = date
        self._id = id

    def id(self):
        return self._id

    def date(self):
        return self._date

all_planet_data = [
    Planet(1, "foo", 50, [Flight(1, '2084-06-01'), Flight(2, '2085-07-14')]),
    Planet(2, "bar", 70, [])
]
all_flight_data = [Flight(1, '2084-06-01'), Flight(2, '2085-07-14')]

def test_all_planets(planet_id=None):
    return list(filter(
        lambda p: planet_id is None or p.id == int(planet_id),
        all_planet_data
    ))

def test_all_flights(flight_id=None):
    return list(filter(
        lambda f: flight_id is None or f.id == int(flight_id),
        all_flight_data
    ))

class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = App(
            args=None,
            all_planets=test_all_planets,
            all_flights=test_all_flights
        )

    def test_all(self):
        self.assertEqual(len(self.app.planets()), 2)

    def test_filter(self):
        self.assertEqual(len(self.app.planets(planet_id=1)), 1)
        self.assertEqual(self.app.planets(planet_id=1)[0]["name"], "foo")

    def test_earliest_flight(self):
        self.assertEqual(self.app.earliest_flight(planet_id=1)["date"], '2084-06-01')
        self.assertEqual(0, len(self.app.earliest_flight(planet_id=2)))
