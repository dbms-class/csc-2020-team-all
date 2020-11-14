## Веб сервер
import cherrypy

from connect import parse_cmd_line
from connect import create_connection
from static import index


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args
        # update_retail(self, 1, 1, 'M1', 1.22)
        # update_retail(self, 1, 2, 'M2', 1.23)

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update_retail(self, medicine_id, pharmacy_id, remainder, price):
        with create_connection(self.args) as db:
            cur = db.cursor()

            cur.execute("SELECT EXISTS(SELECT * FROM Availability WHERE  pharmacy_id = %s and medicine_id = %s)",
                        medicine_id, pharmacy_id)
            result = []
            is_exist = cur.fetchall()
            if is_exist:
                cur.execute(
                    "UPDATE Availability SET remainder = %s, price = %s WHERE  pharmacy_id = %s and medicine_id = %s)",
                    remainder, price, pharmacy_id, medicine_id)
            else:
                cur.execute(
                    "INSERT INTO Availability VALUES(remainder = %s, price = %s WHERE  pharmacy_id = %s and medicine_id = %s)",
                    remainder, price, pharmacy_id, medicine_id)
            return []

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute(
                "SELECT M.id, M.trade_name, A.title as inn FROM Medicine M JOIN Active_Substance A ON M.active_substance_id=A.id")
            result = []
            medicines = cur.fetchall()
            for med in medicines:
                result.append({"id": m[0], "name": m[1], "inn": [2]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, title num, address FROM Pharmacy")
            result = []
            medicines = cur.fetchall()
            for med in medicines:
                result.append({"id": m[0], "num": m[1], "address": [2]})
            return result


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))