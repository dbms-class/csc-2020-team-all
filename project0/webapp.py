# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import connection_factory
from connect import parse_cmd_line
import model
#import model2
from static import index


@cherrypy.expose
class App(object):
    def __init__(self, args, all_planets):
        self.args = args
        self.all_planets = all_planets

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def planets(self, planet_id=None):
        return list(map(
            lambda p: {
                "id": p.id,
                "name": p.get_name(),
                "distance": int(p.get_distance()),
                "flight_count": p.get_flight_count()
            },
            filter(
                lambda p: planet_id is None or p.id == int(planet_id),
                self.all_planets()
            )
        ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def planets2(self, planet_id=None):
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
        all_planets=model.all_planets
    ))
