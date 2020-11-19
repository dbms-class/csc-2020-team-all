# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import connection_factory
from connect import parse_cmd_line

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
    def stops(self):
      db = connection_factory.getconn()
      try:
        cur = db.cursor()
        cur.execute("SELECT id, address, available_platforms FROM stop S;")
        stops = cur.fetchall()
        result = [
          {"id": p[0], "address": p[1], "platforms": p[2]}
          for s in stops
        ]
        return result
      finally:
        connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def routes(self):
      db = connection_factory.getconn()
      try:
          cur = db.cursor()
          cur.execute("SELECT id, initial_stop, final_stop FROM route R;")
          routes = cur.fetchall()
          result = [
            {"route": p[0], "start_stop_id": p[1], "end_stop_id": p[2]}
            for r in routes
          ]
          return result
      finally:
        connection_factory.putconn(db)

    @cherrypy.expose
    def update_timetable(self, stop_id, platform, time, route_id, is_working_day):
      db = connection_factory.getconn()
      try:
          cur = db.cursor()
          print("POST PARAMS: {0}, {1}, {2}, {3}, {4}".format(stop_id, platform, time, route_id, is_working_day))
          # бага
          cur.execute("INSERT INTO timetable(stop_id, time, route_id, platform_number, is_weekend) VALUES(%s, %s, %s, %s, %s);".format(stop_id, time, route_id, platform, 
          is_working_day))
      finally:
        connection_factory.putconn(db)


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))

