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


def all_flights(flight_id=None, load_commander=False):
    db = connection_factory.getconn()
    try:
        tab_flight = Table('flight').bind(db)
        tab_commander = Table('commander').bind(db)
        if load_commander:
            q = tab_flight.select(
                tab_flight.c.id,
                tab_flight.c.date,
                tab_commander.c.id.alias('commander_id'),
                tab_commander.c.name.alias('commander_name')).join(
                    tab_commander, on=(tab_flight.c.commander_id == tab_commander.c.id))
        else:
            q = tab_flight.select(tab_flight.c.id, tab_flight.c.date, tab_flight.c.commander_id)

        if flight_id is not None:
            q = q.where(tab_flight.c.id == flight_id)
        q = q.objects(Flight)
        return [f for f in q]
    finally:
        connection_factory.putconn(db)


def txn(work):
    db = connection_factory.getconn()
    try:
        with db.atomic() as txn:
            return work(db)
    finally:
        connection_factory.putconn(db)

pg_db = PostgresqlDatabase('postgres', user='postgres', password='',
                   host='127.0.0.1', port=5432)

class PlanetEntity(Model):
    id = AutoField()
    name = CharField()
    avg_distance = DecimalField()
    flight_count = IntegerField()

    class Meta:
        database = pg_db
        table_name = 'planetview'


class CommanderEntity(Model):
    id = AutoField()
    name = CharField()


class FlightEntity(Model):
    commander = ForeignKeyField(CommanderEntity, backref="flights", column_name="commnader_id")


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

    def set_distance(self, distance, flight_date):
        return txn(lambda db: self.set_distance_work(db, distance, flight_date))

    def set_distance_work(self, db, distance, flight_date):
        f = Table('flight').bind(db)
        rowcount = f.update(distance=distance).where(f.c.planet_id == self.id and f.c.date == flight_date).execute()
        if rowcount > 0:
            return True

        nextId = f.select(fn.MAX(f.c.id)).scalar() + 1
        f.insert(id=nextId, planet_id=self.id, date=flight_date).execute()
        return f.update(distance=distance).where(f.c.id == nextId).execute() == 1

    def set_distance_work_old(self, db, distance, flight_date):
        cur = db.cursor()
        cur.execute("UPDATE Flight SET distance=%s WHERE planet_id=%s AND date=%s", (distance, self.id, flight_date))
        if cur.rowcount > 0:
            return True
        cur.execute("SELECT MAX(id) FROM Flight")
        maxId = cur.fetchone()[0]
        cur.execute("INSERT INTO Flight (id, planet_id, date) VALUES (%s, %s, %s)", (maxId + 1, self.id, flight_date))
        if cur.rowcount == 0:
            return False
        cur.execute("UPDATE Flight SET distance=%s WHERE planet_id=%s AND date=%s", (distance, self.id, flight_date))
        result = cur.rowcount > 0
        return result

class Flight:
    def __init__(self, id, date, commander_id=None, commander_name=None, spacecraft_id=None, spacecraft_name=None):
        self.spacecraft_name = spacecraft_name
        self.spacecraft_id = spacecraft_id
        self.commander_name = commander_name
        self.commander_id = commander_id
        self.date = date
        self.id = id


    def commander(self):
        if self.commander_name is not None:
            return self.commander_name
        db = connection_factory.getconn()
        try:
            c = Table('commander').bind(db)
            if self.commander_id is not None:
                return c.select(c.c.name).where(c.c.id == self.commander_id).get()

            f = Table('flight').bind(db)
            return c.join(f).select(c.c.name).where(f.c.id == self.id).get()
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
