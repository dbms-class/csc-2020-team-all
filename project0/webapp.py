# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import connection_factory
from connect import parse_cmd_line
#import model2 as model
import model3 as model
from static import index


@cherrypy.expose
class App(object):
    def __init__(self, args, all_planets, all_flights):
        self.args = args
        self.all_planets = all_planets
        self.all_flights = all_flights

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def flights(self, flight_id=None, load_commander=True):
        def to_json(f):
            base = {"id": f.id(), "date": str(f.date())}
            if load_commander:
               base.update({"commander": f.commander()})
            return base

        return list(map(
            to_json,
            self.all_flights(flight_id, load_commander)
        ))

    # @cherrypy.expose
    # @cherrypy.tools.json_out()
    # def planets(self, planet_id=None):
    #     return list(map(
    #         lambda p: {
    #             "id": p.id,
    #             "name": p.name,
    #             "distance": int(p.avg_distance),
    #             "flight_count": p.flight_count
    #         },
    #         model.PlanetEntity.select()
    #     ))

    def planets(self, planet_id=None):
        return list(map(
            lambda p: {
                "id": p.id,
                "name": p.get_name(),
                "distance": int(p.get_distance()),
                "flight_count": p.get_flight_count()
            },
            self.all_planets(planet_id=planet_id)
        ))

    @cherrypy.expose
    def set_distance(self, planet_id, distance, date):
        planet = self.all_planets(planet_id=planet_id)
        if len(planet) == 0:
            raise cherrypy.HTTPError(404)
        is_ok = planet[0].set_distance(distance, date)
        if not is_ok:
            raise cherrypy.HTTPError(400)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def commanders(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Commander")
            result = []
            commanders = cur.fetchall()
            for c in commanders:
                result.append({"id": c[0], "name": c[1]})
            return result
        finally:
            connection_factory.putconn(db)


if __name__ == "__main__":
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
    })
    cherrypy.quickstart(App(
        args=parse_cmd_line(),
        all_planets=model.all_planets,
        all_flights=model.all_flights
    ))
