from connect import connection_factory

from peewee import *


def all_planets(planet_id = None):
    db = connection_factory.getconn()
    try:
        PlanetView = Table('planetview').bind(db)
        q = PlanetView.select(PlanetView.c.id, PlanetView.c.name, PlanetView.c.avg_distance, PlanetView.c.flight_count)
        if planet_id is not None:
            q = q.where(PlanetView.c.id == planet_id)
        q = q.objects(Planet)
        return [p for p in q]
    finally:
        connection_factory.putconn(db)


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
