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
    @cherrypy.tools.json_out()
    def stops(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, address, available_platforms FROM stop S;")
            planets = cur.fetchall()
            result = [
              {"id": p[0], "address": p[1], "platforms": p[2]}
              for p in planets
            ]
            return result


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))

