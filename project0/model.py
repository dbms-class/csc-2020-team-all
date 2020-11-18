from connect import connection_factory

def all_planets():
    db = connection_factory.getconn()
    try:
        cur = db.cursor()
        cur.execute("SELECT id FROM Planet")
        result = []
        for p in cur.fetchall():
            result.append(Planet(p[0]))
        return result
    finally:
        connection_factory.putconn(db)


class Planet:
    def __init__(self, id):
        self.id = id

    def name(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(
                "SELECT name FROM Planet WHERE id=%s", (self.id,)
            )
            return cur.fetchone()[0]
        finally:
            connection_factory.putconn(db)

    def distance(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(
                "SELECT distance FROM Planet WHERE id=%s", (self.id,)
            )
            return cur.fetchone()[0]
        finally:
            connection_factory.putconn(db)

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

    def flight_count(self):
        return len(self.flights())


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
