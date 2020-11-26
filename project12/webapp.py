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
    def update_retail(self, drug_id, pharmacy_id, remainder, price):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query = """
                UPDATE Availability
                SET price={price}, remainder={remainder}
                WHERE pharmacy_id={pharmacy_id} AND medicine_id={drug_id};
                INSERT INTO Availability(pharmacy_id, medicine_id, price, remainder)
                SELECT {pharmacy_id}, {drug_id}, {price}, {remainder}
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM Availability
                    WHERE pharmacy_id={pharmacy_id} AND medicine_id={drug_id}
                )
            """.format(drug_id=drug_id, pharmacy_id=pharmacy_id, remainder=remainder, price=price)
            cur.execute(query)
            return {"status": "OK"}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query = """
                SELECT M.id, M.trade_name, A.title as inn
                FROM Medicine M JOIN ActiveSubstance A
                ON M.active_substance_id=A.id
            """
            cur.execute(query)
            result = []
            medicines = cur.fetchall()
            for m in medicines:
                result.append({"id": m[0], "trade_name": m[1], "inn": m[2]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query = """
                SELECT id, title num, address
                FROM Pharmacy
            """
            cur.execute(query)
            result = []
            medicines = cur.fetchall()
            for m in medicines:
                result.append({"id": m[0], "num": m[1], "address": m[2]})
            return result


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
