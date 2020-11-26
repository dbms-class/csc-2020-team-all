# encoding: UTF-8

import json

import cherrypy
import cherrypy_cors

from connect import parse_cmd_line
from connect import create_connection

@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def index(self):
        return "Hello web app"

    @cherrypy.expose
    @cherrypy.config()
    def bands(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("select id, name, location from bands_view")
            result = []
            bands_info = cur.fetchall()
            for b in bands_info:
                result.append({"id": b[0], "name": b[1], "location": b[2]})
            return json.dumps(result, ensure_ascii=False).encode('utf8')


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))