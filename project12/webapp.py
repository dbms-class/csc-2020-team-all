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
            stocks = Table('medicinestocks').bind(db)

            min_max_price = stocks.select(
                stocks.c.drug_id,
                fn.MIN(stocks.c.price).alias('min_price'),
                fn.MAX(stocks.c.price).alias('max_price')
            ).group_by(stocks.c.drug_id)

            query = stocks.select(
                stocks.c.drug_id,
                stocks.c.drug_trade_name,
                stocks.c.drug_inn,
                stocks.c.pharmacy_id,
                stocks.c.pharmacy_address,
                stocks.c.remainder,
                stocks.c.price,
                min_max_price.c.min_price,
                min_max_price.c.max_price
            ).join(
                min_max_price, on=(stocks.c.drug_id == min_max_price.c.drug_id)
            )

            if drug_id is not None:
                query = query.where(stocks.c.drug_id == drug_id)

            if min_remainder is not None:
                query = query.where(stocks.c.remainder >= min_remainder)

            if max_price is not None:
                query = query.where(stocks.c.price <= max_price)

            query = query.order_by(stocks.c.drug_id, stocks.c.pharmacy_id)

            result = list(query.execute())
            return result

@cherrypy.expose
@cherrypy.tools.json_out()
def drug_move(self, drug_id, min_remainder, target_income_increase):
  with self.connection_factory.conn() as db:
    cur = db.cursor()

    # достаем всех, у кого положительный излишек
    query = f'''
        SELECT remainder - min_remainder AS diff, pharmacy_id, price
        FROM Availability 
        WHERE remainder > min_remainder AND medicine_id = {drug_id}
        ORDER BY price 
    '''
    cur.execute(query)
    pos_info = cur.fetchall()

    # достать всех, у кого отрицательный излишек
    query = f'''
        SELECT remainder - min_remainder AS diff, pharmacy_id, price
        FROM Availability 
        WHERE remainder < min_remainder AND medicine_id = {drug_id}
        ORDER BY price DESC
    '''
    cur.execute(query)
    neg_info = cur.fetchall()
    
    # перераспределить излишки + посчитать прибыль
    # TODO: учитывать target_income_increase
    income_increase = 0
    pos_i = 0
    neg_i = 0

    while (pos_i < len(pos_info) and neg_i < len(neg_info)):
        if (pos_info[pos_i][2] >= neg_info[neg_i][2]): 
          break
        price_inc = neg_info[neg_i][2] - pos_info[pos_i][2] 
        diff = min(-neg_info[neg_i][0], pos_info[pos_i][0])
        income_increase += diff * price_inc
        pos_info[pos_i] = (pos_info[pos_i][0] - diff, pos_info[pos_i][1], pos_info[pos_i][2])
        neg_info[neg_i] = (neg_info[neg_i][0] + diff, neg_info[neg_i][1], neg_info[neg_i][2])
        if (pos_info[pos_i][0] == 0): 
           pos_i += 1
        if (neg_info[neg_i][0] == 0):
           neg_i += 1
            
    # update
    # всем аптекам, у кого info[i][0] == 0 - выставляем min_remainder
    query = f'''
      UPDATE Availability
      SET remainder = {min_remainder}
      WHERE
    '''
    # TODO: тут append к query нужных id-шников аптек

    # TODO: + два апдейта на случай, если были частичные перекладывания (имеет смысл добавить на это флажки, чтобы не делать их просто так)



cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))