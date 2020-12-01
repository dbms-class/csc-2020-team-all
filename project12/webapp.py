## Веб сервер
import cherrypy

from connect import create_connection_factory
from connect import parse_cmd_line
from static import index


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.connection_factory = create_connection_factory(args)

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update_retail(self, drug_id, pharmacy_id, remainder, price):
        with self.connection_factory.conn() as db:
            cur = db.cursor()
            query = """
                SELECT pharmacy_id
                FROM Availability
                WHERE pharmacy_id=%(pharmacy_id)s AND medicine_id=%(drug_id)s;
            """
            cur.execute(query, {
                'drug_id': drug_id,
                'pharmacy_id': pharmacy_id,
            })

            if cur.fetchone() is not None:
                status = 'updated'
                query = """
                    UPDATE Availability
                    SET price=%(price)s, remainder=%(remainder)s
                    WHERE pharmacy_id=%(pharmacy_id)s AND medicine_id=%(drug_id)s;
                """
            else:
                status = 'inserted'
                query = """
                    INSERT INTO Availability(pharmacy_id, medicine_id, price, remainder)
                    VALUES (%(pharmacy_id)s, %(drug_id)s, %(price)s, %(remainder)s);
                """
            cur.execute(query, {
                'drug_id': drug_id,
                'pharmacy_id': pharmacy_id,
                'remainder': remainder,
                'price': price
            })
            db.commit()
            return {0: 'OK', 'status': status}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        with self.connection_factory.conn() as db:
            cur = db.cursor()
            query = """
                SELECT id, trade_name, international_trade_name
                FROM Medicine
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
        with self.connection_factory.conn() as db:
            cur = db.cursor()
            query = """
                SELECT id, title, address
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
