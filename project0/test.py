import unittest

from webapp import App
from model2 import Planet


def test_all_planets():
    return [Planet(1, "foo", 50, 3), Planet(2, "bar", 70, 0)]


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = App(
            args=None,
            all_planets=test_all_planets
        )

    def test_all(self):
        self.assertEqual(len(self.app.planets()), 2)

    def test_filter(self):
        self.assertEqual(len(self.app.planets(planet_id=1)), 1)
        self.assertEqual(self.app.planets(planet_id=1)[0]["name"], "foo")
