
# encoding: UTF-8

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
    @cherrypy.tools.json_out()
    def update_retail(self, drug_id, pharmacy_id, remainder, price):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("insert into drugstore_price_list(drugstore_id, drug_id, price,items_count) values (%s, %s, %s, %s) on conflict (drugstore_id, drug_id) do update set items_count = %s", (pharmacy_id, drug_id, price, remainder, remainder))
            

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("select id, trademark, international_name from drug")
            result = []
            drugs = cur.fetchall()
            for d in drugs:
                result.append({"id": d[0], "trademark": d[1], "international_name": d[2]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("select id, name, address from drugstore")
            result = []
            drugstores = cur.fetchall()
            for d in drugstores:
                result.append({"id": d[0], "name": d[1], "address": d[2]})
            return result

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
