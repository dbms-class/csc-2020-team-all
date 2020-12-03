from connect import connection_factory
from copy import copy
from peewee import *


class Stop:
    def __init__(self, id, address, number_of_platforms):
        self.id = id
        self.address = address
        self.number_of_platforms = number_of_platforms

    def get_address(self):
        return self.address

    def get_id(self):
        return self.id

    def get_number_of_platforms(self):
        return self.number_of_platforms

class Route:
    def __init__(self, id, route, transport_type_id, first_stop_id, last_stop_id):
        self.id = id
        self.route = route
        self.transport_type_id = transport_type_id
        self.first_stop_id = first_stop_id
        self.last_stop_id = last_stop_id

# route_id INT NOT NULL references transport_route, --есть описание маршрута с таким айди N:M
# stop_id INT NOT NULL references transport_stop, --есть одна такая остановка по айди остановки N:M
# platform_number INT NOT NULL check(platform_number >= 1),
# arrival_time TIME NOT NULL,
# is_working_day BOOLEAN NOT NULL,
class RouteStop:
    def __init__(self, route_id, stop_id, platform_number, arrival_time, is_working_day):
        self.route_id = route_id
        self.stop_id = stop_id
        self.platform_number = platform_number
        self.arrival_time = arrival_time
        self.is_working_day = is_working_day


class Planet:
    def __init__(self, id, name, avg_distance, flight_count):
        self.id = id
        self.name = name
        self.distance = avg_distance
        self.flight_count = flight_count

    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance

    def flights(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(
                "SELECT id FROM Flight WHERE planet_id=%s", (self.id,)
            )
            result = []
            for f in cur.fetchall():
                result.append(Flight(f[0]))
            return result
        finally:
            connection_factory.putconn(db)

    def get_flight_count(self):
        return self.flight_count

    def txn(self, work):
        db = connection_factory.getconn()
        try:
            with db.atomic() as txn:
                return work(db)
        finally:
            connection_factory.putconn(db)

    def set_distance(self, distance, flight_date):
        return self.txn(lambda db: self.set_distance_work(db, distance, flight_date))

    def set_distance_work(self, db, distance, flight_date):
        f = Table('flight').bind(db)
        rowcount = f.update(distance=distance).where(f.c.planet_id == self.id and f.c.date == flight_date).execute()
        if rowcount > 0:
            return True

        nextId = f.select(fn.MAX(f.c.id)).scalar() + 1
        f.insert(id=nextId, planet_id=self.id, date=flight_date).execute()
        return f.update(distance=distance).where(f.c.id == nextId).execute() == 1


class Flight:
    def __init__(self, id):
        self.id = id
        self.commander = self._commander()
        self.spacecraft = self._spacecraft()

    def _commander(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute("SELECT commander_id FROM Flight WHERE id=%s", (self.id,))
            commander_id = cur.fetchone()[0]
            cur.execute("SELECT name FROM Commander WHERE id=%s", (commander_id,))
            return cur.fetchone()[0]
        finally:
            connection_factory.putconn(db)

    def _spacecraft(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute("SELECT spacecraft_id FROM Flight WHERE id=%s", (self.id,))
            spacecraft_id = cur.fetchone()[0]
            cur.execute("SELECT name FROM Spacecraft WHERE id=%s", (spacecraft_id,))
            return cur.fetchone()[0]
        finally:
            connection_factory.putconn(db)