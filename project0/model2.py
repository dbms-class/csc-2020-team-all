from connect import connection_factory

def all_planets(planet_id = None):
    db = connection_factory.getconn()
    try:
        cur = db.cursor()
        if planet_id is None:
            cur.execute("SELECT id, name, avg_distance, flight_count FROM PlanetView")
        else:
            cur.execute("SELECT id, name, avg_distance, flight_count FROM PlanetView WHERE id=%s", (planet_id,))
        result = []
        for p in cur.fetchall():
            result.append(Planet(p[0], p[1], p[2], p[3]))
        return result
    finally:
        connection_factory.putconn(db)


class Planet:
    def __init__(self, id, name, distance, flight_count):
        self.id = id
        self.name = name
        self.distance = distance
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
            return work(db)
        finally:
            db.commit()
            connection_factory.putconn(db)

    def set_distance(self, distance, flight_date):
        return self.txn(lambda db: self.set_distance_work(db, distance, flight_date))

    def set_distance_work(self, db, distance, flight_date):
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
