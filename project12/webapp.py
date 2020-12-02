"""Server app
"""
import cherrypy

from connect import create_connection_factory
from connect import parse_cmd_line
from static import index

from peewee import *


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.connection_factory = create_connection_factory(args)

    @cherrypy.expose
    def start(self):
        return 'Hello web app'

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
    def update_retail_builder(self, drug_id, pharmacy_id, remainder, price):
        with self.connection_factory.conn() as db:
            availability = Table('availability').bind(db)
            columns = availability.c
            query = availability.select(
                columns.pharmacy_id
            ).where(
                columns.pharmacy_id == pharmacy_id,
                columns.medicine_id == drug_id
            )

            if query.exists():
                status = 'updated'
                query = availability.update(
                    price=price,
                    remainder=remainder,
                ).where(
                    columns.pharmacy_id == pharmacy_id,
                    columns.medicine_id == drug_id
                )
            else:
                status = 'inserted'
                query = availability.insert(
                    pharmacy_id=pharmacy_id,
                    medicine_id=drug_id,
                    price=price,
                    remainder=remainder,
                )

            query.execute()
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
                result.append({'id': m[0], 'trade_name': m[1], 'inn': m[2]})
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
                result.append({'id': m[0], 'num': m[1], 'address': m[2]})
            return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status_retail(self, drug_id=None, min_remainder=None, max_price=None):
        with self.connection_factory.conn() as db:
            availability = Table('availability').bind(db)
            medicine = Table('medicine').bind(db)
            pharmacy = Table('pharmacy').bind(db)

            min_max_price = availability.select(
                availability.c.medicine_id,
                fn.MIN(availability.c.price),
                fn.MAX(availability.c.price)
            ).group_by(availability.c.medicine_id)

            query = availability.select(
                availability.c.medicine_id.alias('drug_id'),
                medicine.c.trade_name.alias('drug_trade_name'),
                medicine.c.international_trade_name.alias('drug_inn'),
                availability.c.pharmacy_id.alias('pharmacy_id'),
                pharmacy.c.address.alias('pharmacy_address'),
                availability.c.remainder.alias('remainder'),
                availability.c.price.alias('price'),
                min_max_price.c.min.alias('min_price'),
                min_max_price.c.max.alias('max_price')
            ).join(
                medicine, on=(availability.c.medicine_id == medicine.c.id)
            ).join(
                pharmacy, on=(availability.c.pharmacy_id == pharmacy.c.id)
            ).join(
                min_max_price, on=(availability.c.medicine_id == min_max_price.c.medicine_id)
            )

            if drug_id is not None:
                query = query.where(availability.c.medicine_id == drug_id)

            if min_remainder is not None:
                query = query.where(availability.c.remainder >= min_remainder)

            if max_price is not None:
                query = query.where(availability.c.price <= max_price)

            stocks = list(query.execute())
            return stocks


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
