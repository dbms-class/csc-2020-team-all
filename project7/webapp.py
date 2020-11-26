
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
              result.append({
                "id": d[0],
                "name": d[1],
                "address": d[2]
              })
          return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status_retail(self, drug_id=None, min_remainder=None, max_price=None):
        with create_connection(self.args) as db:
          cur = db.cursor()
          sql_querry = """
            select * from (select 
            L.drug_id as drug_id,
            D.trademark as drug_trade_name,
            D.international_name as drug_inn,
            L.drugstore_id as pharmacy_id,
            DS.address as pharmacy_address,
            L.items_count as remainder,
            L.price as price
            from drugstore_price_list L 
            left join drugstore DS on drugstore_id = id
            left join drug D on drug_id = D.id) U
            left join (select
            drug_id,
            MIN(price) as min_price,
            MAX(price) as max_price
            from drugstore_price_list L
            group by drug_id) V on U.drug_id = V.drug_id"""

          query_filters = []
          if (drug_id):
            query_filters.append("drug_id")
          if (min_remainder):
            query_filters.append("min_remainder")
          if (max_price):
            query_filters.append("max_price")

          if query_filters:
            sql_querry += "\n where U.%s ".format(qf)
          for ind, qf in enumerate(query_filters):
            sql_querry += qf
            if qf == "drug_id":
              sql_querry += "=".format(drug_id)
            elif qf == "remainder":
              sql_querry += ">= ".format(remainder)
            elif qf == "price":
              sql_querry += "<= ".format(price)
            if ind != len(query_filters):
              sql_querry += " and "

          cur.execute(sql_querry)
          result = []
          drugstores = cur.fetchall()
          for d in drugstores:
            result.append({
              "drug_id": d[0],
              "drug_trade_name": d[1],
              "drug_inn": d[2],
              "pharmacy_id": d[3],
              "pharmacy_address": d[4],
              "remainder": d[5],
              "price": float(d[6]),
              "min_price": float(d[8]),
              "max_price": float(d[9])
            })

          print(result)
          return result

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
