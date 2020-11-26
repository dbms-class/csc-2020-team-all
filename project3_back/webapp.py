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


    # check in
    # https://csc-2020-team-all-3.dmitrybarashev.repl.co/update_price/1/1/1
    
    # command to run
    # python3 webapp.py --sqlite-file="sqlite.db"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update_price(self, apartment_id, week, price):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT EXISTS (SELECT * FROM Price WHERE apartment_id=%s AND week=%s)" % (apartment_id, week))
            exists = cur.fetchall()
            if exists:
              cur.execute("UPDATE Price SET price=%s WHERE apartment_id=%s AND week=%s" % (price, apartment_id, week))
            else:
              # TBD consider remove
              cur.execute("INSERT INTO Price VALUES (%s, %s, %s)" % (price, apartment_id, week))
            result = []
            # planets = cur.fetchall()
            # for p in planets:
            #     result.append({"id": p[0], "name": p[1]})
            return "UPDATE DONE"

    # @cherrypy.expose
    # @cherrypy.tools.json_out()
    # def commanders(self):
    #     with create_connection(self.args) as db:
    #         cur = db.cursor()
    #         cur.execute("SELECT id, name FROM Commander")
    #         result = []
    #         commanders = cur.fetchall()
    #         for c in commanders:
    #             result.append({"id": c[0], "name": c[1]})
    #         return result


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))

