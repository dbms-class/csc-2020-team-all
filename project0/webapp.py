# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import connection_factory
from connect import parse_cmd_line
from model import all_planets
from static import index


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

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
                "name": p.name(),
                "distance": int(p.distance()),
                "flight_count": p.flight_count()
            },
            filter(
                lambda p: planet_id is None or p.id == int(planet_id),
                all_planets()
            )
        ))


    # def planets2(self, planet_id=None):
    #     return list(map(
    #         lambda p: {"id": p.id, "name": p.name(), "distance": int(p.distance()), "flight_count": p.flight_count()},
    #         filter(
    #             lambda p: planet_id is None or p.id == planet_id,
    #             all_planets()
    #         )
    #     ))
    #
    def planets1(self, planet_id=None):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            if planet_id is None:
                cur.execute("SELECT id, name FROM Planet P")
            else:
                cur.execute("SELECT id, name FROM Planet WHERE id= %s", planet_id)
            result = []
            planets = cur.fetchall()
            for p in planets:
                result.append({"id": p[0], "name": p[1]})
            return result
        finally:
            connection_factory.putconn(db)

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


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
