from connect import connection_factory
import logging
from psycopg2.extras import LoggingConnection

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from peewee import *

class LoggingDatabase(PostgresqlDatabase):
    def __init__(self, database, register_unicode=True, encoding=None,
             isolation_level=None, **kwargs):
        super(LoggingDatabase, self).__init__(
            'postgres', user='postgres', password='', host='127.0.0.1', port=5432,
            connection_factory=LoggingConnection)

    def _connect(self):
        conn = super(LoggingDatabase, self)._connect()
        conn.initialize(logger)
        return conn

pg_db = LoggingDatabase("postgres")

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

    class Meta:
        database = pg_db
        table_name = 'commander'


class FlightEntity(Model):
    id = IntegerField(unique=True)
    date = DateField()
    planet = ForeignKeyField(PlanetEntity, backref="flights", column_name="planet_id")
    commander = ForeignKeyField(CommanderEntity, backref="flights", column_name="commander_id")

    class Meta:
        database = pg_db
        table_name = 'flight'


def all_planets(planet_id=None):
    q = PlanetEntity.select()
    if planet_id is not None:
        q = q.where(PlanetEntity.id == planet_id)
    return [Planet(p) for p in q]


def all_flights(flight_id=None, load_commander=False):
    if load_commander:
        q = FlightEntity.select(FlightEntity.id, FlightEntity.date, CommanderEntity.name).join(CommanderEntity)
    else:
        q = FlightEntity.select()
    if flight_id is not None:
        q = q.where(FlightEntity.id == flight_id)
    return [Flight(f) for f in q]

def txn(work):
    db = connection_factory.getconn()
    try:
        with pg_db.atomic() as txn:
            return work(db)
    finally:
        connection_factory.putconn(db)


class Planet:
    def __init__(self, entity):
        self.entity = entity

    def get_name(self):
        return self.entity.name

    def get_distance(self):
        return self.entity.avg_distance

    def flights(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(
                "SELECT id FROM Flight WHERE planet_id=%s", (self.entity.id,)
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


class Flight:
    def __init__(self, flight_entity):
        self.flight_entity = flight_entity

    def id(self):
        return self.flight_entity.id

    def date(self):
        return self.flight_entity.date

    def commander(self):
        return self.flight_entity.commander.name

    def spacecraft(self):
        return self.flight_entity.spacecraft.name
