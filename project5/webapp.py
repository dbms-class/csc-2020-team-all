# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import parse_cmd_line
from connect import create_connection
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
    def update_timetable(self, stop_id, platform, _time, route_id, is_working_day=1):
      if (!is_working_day.isnumeric() and (int(is_working_day) not in [0, 1]) return
      if (!stop_id.isnumeric()) return
      if (!platform.isnumeric()) return
      if (!_time.isnumeric() && !(1 <= int(_time) <= 1440)) return
      if (!route_id.isnumeric()) return

      db = create_connection(self.args)
      cur = db.cursor()
      cur.execute(f"SELECT * FROM route_stop WHERE route_id={route_id} \
                    and stop_id={stop_id} \
                    and platform_number={platform} \
                    and is_working_day={True if is_working_day else False};")
      result = cur.fetchall()

      if len(result) == 0: 
        cur.execute(f"INSERT INTO \
                      route_stop (route_id, stop_id, platform_number, arrival_time, is_working_day) \
                      VALUES({route_id}, \
                             {stop_id}, \
                             {platform}, \
                             interval '{_time} minute'::TIME, \
                             {True if is_working_day else False};"
                    )
      else:
        cur.execute(f"UPDATE route_stop \
                      SET arrival_time = interval '{_time} minute'::TIME \
                      WHERE route_id={route_id} \
                        and stop_id={stop_id} \
                        and platform_number={platform} \
                        and is_working_day={True if is_working_day else False};"
                    )

      cur.close()
      return

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def routes(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, route, first_stop_id, last_stop_id FROM transport_route")
            result = []
            routes = cur.fetchall()
            for r in routes:
              result.append({"id": r[0], "route": r[1],"start_stop_id": r[2], "end_stop_id": r[3]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stops(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, address, number_of_platforms FROM transport_stop")
            result = []
            stops = cur.fetchall()
            for s in stops:
              result.append({"id": s[0], "address": s[1],"number_of_platforms": s[2]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def planets(self, planet_id = None):
        with create_connection(self.args) as db:
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
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def commanders(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Commander")
            result = []
            commanders = cur.fetchall()
            for c in commanders:
                result.append({"id": c[0], "name": c[1]})
            return result



cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
