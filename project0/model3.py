from connect import connection_factory
from peewee import *

db = connection_factory.create_db()


class PlanetEntity(Model):
    id = AutoField()
    name = CharField()
    avg_distance = DecimalField()
    flight_count = IntegerField()

    class Meta:
        database = db
        table_name = 'planetview'


class CommanderEntity(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        database = db
        table_name = 'commander'


class FlightEntity(Model):
    id = IntegerField(unique=True)
    date = DateField()
    planet = ForeignKeyField(PlanetEntity, backref="flights", column_name="planet_id")
    commander = ForeignKeyField(CommanderEntity, backref="flights", column_name="commander_id")

    class Meta:
        database = db
        table_name = 'flight'


def all_planets(planet_id=None):
    q = PlanetEntity.select()
    if planet_id is not None:
        q = q.where(PlanetEntity.id == planet_id)
    return [Planet(p) for p in q]


# def all_flights(flight_id=None, load_commander=False):
#     q = FlightEntity.select()
#     if flight_id is not None:
#         q = q.where(FlightEntity.id == flight_id)
#     return [Flight(entity=f) for f in q]

def all_flights(flight_id=None, load_commander=False):
    if load_commander:
        q = FlightEntity.select(FlightEntity.id, FlightEntity.date, CommanderEntity.name).join(CommanderEntity)
    else:
        q = FlightEntity.select()
    if flight_id is not None:
        q = q.where(FlightEntity.id == flight_id)
    return [Flight(entity=f) for f in q]


def txn(work):
    with db.atomic() as txn:
        return work(db)


class Planet:
    def __init__(self, entity):
        self.entity = entity
        self.id = entity.id

    def get_name(self):
        return self.entity.name

    def get_distance(self):
        return self.entity.avg_distance

    def get_flight_count(self):
        return self.entity.flight_count

    def flights(self):
        def work(db):
            cur = db.cursor()
            cur.execute(
                "SELECT id FROM Flight WHERE planet_id=%s", (self.entity.id,)
            )
            result = []
            for f in cur.fetchall():
                result.append(Flight(id=f[0]))
            return result
        return txn(work)

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
    def __init__(self, entity=None, id=None):
        self.entity = entity
        self._id = id

    def _entity(self):
        return self.entity if self.entity is not None else FlightEntity.get_by_id(self._id)

    def id(self):
        return self._id if self._id is not None else self._entity().id

    def date(self):
        return self._entity().date

    def commander(self):
        return self._entity().commander.name

    def spacecraft(self):
        return self._entity().spacecraft.name
