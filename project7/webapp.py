# encoding: UTF-8

import cherrypy
from connect import parse_cmd_line
from connect import create_connection_factory

from peewee import *

import json
from decimal import Decimal

class _JSONEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    return super().default(obj)
  def iterencode(self, value):
    # Adapted from cherrypy/_cpcompat.py
    for chunk in super().iterencode(value):
      yield chunk.encode("utf-8")

json_encoder = _JSONEncoder()

def json_handler(*args, **kwargs):
  # Adapted from cherrypy/lib/jsontools.py
  value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
  return json_encoder.iterencode(value)

@cherrypy.expose
class App(object):
    def __init__(self, args):
      self.connection_factory = create_connection_factory(args)

    @cherrypy.expose
    def index(self):
      return "Hello web app"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
      with self.connection_factory.conn() as db:
        cur = db.cursor()
        cur.execute("select id, trademark, international_name from drug")
        result = []
        drugs = cur.fetchall()
        for d in drugs:
            result.append({"id": d[0], "trademark": d[1], "international_name": d[2]})
        return result
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs_peewe(self):
      with self.connection_factory.conn() as db:
        drug_table = Table('drug').bind(db)
        d = drug_table.select(
          drug_table.c.id,
          drug_table.c.trademark,
          drug_table.c.international_name
        )
        return list(d.execute())

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
      with self.connection_factory.conn() as db:
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
    def pharmacies_peewe(self):
      with self.connection_factory.conn() as db:
        pharmacy_table = Table('drugstore').bind(db)
        p = pharmacy_table.select(
          pharmacy_table.c.id,
          pharmacy_table.c.name,
          pharmacy_table.c.address
        )
        return list(p.execute())

    @cherrypy.expose
    @cherrypy.tools.json_out(handler=json_handler)
    def status_retail(self, drug_id = None, min_remainder = None, max_price = None):
      with self.connection_factory.conn() as db:
        prices_table = Table('drugstore_price_list').bind(db)
        pharmacy_table = Table('drugstore').bind(db)
        drug_table = Table('drug').bind(db)

        #можно сделать представление, но надо ли?
        drugs_min_max_price = prices_table.select(
          prices_table.c.drug_id,
          fn.MIN(prices_table.c.price).alias('min_price'),
          fn.MAX(prices_table.c.price).alias('max_price')
        ).group_by(prices_table.c.drug_id)

        #можно сделать представление
        q = prices_table.select(
          prices_table.c.drug_id,
          drug_table.c.trademark,
          drug_table.c.international_name,
          prices_table.c.drugstore_id,
          pharmacy_table.c.address,
          prices_table.c.items_count#,
          # prices_table.c.price,
          # drugs_min_max_price.c.min_price,
          # drugs_min_max_price.c.max_price
        ).join(
          drug_table, on=(prices_table.c.drug_id == drug_table.c.id)
        ).join(
          pharmacy_table, on=(prices_table.c.drugstore_id == pharmacy_table.c.id)
        ).join(
          drugs_min_max_price, on=(prices_table.c.drug_id == drugs_min_max_price.c.drug_id)
        )

        if drug_id is not None:
          q = q.where(prices_table.c.drug_id == drug_id)
        
        if min_remainder is not None:
          q = q.where(prices_table.c.items_count >= min_remainder)
        
        if max_price is not None:
          q = q.where(prices_table.c.price <= max_price)

        return list(q.execute())
  
    @cherrypy.expose
    @cherrypy.tools.json_out(handler=json_handler)
    def status_retail_with_table_view(self, drug_id = None, min_remainder = None, max_price = None):
      with self.connection_factory.conn() as db:
        status_retail_table = Table('status_retail').bind(db)
        
        q = status_retail_table.select(
          status_retail_table.c.drug_id,
          status_retail_table.c.drug_trade_name,
          status_retail_table.c.drug_inn,
          status_retail_table.c.pharmacy_id,
          status_retail_table.c.pharmacy_address,
          status_retail_table.c.remainder,
          status_retail_table.c.price,
          status_retail_table.c.min_price,
          status_retail_table.c.max_price
        )

        if drug_id is not None:
          q = q.where(status_retail_table.c.drug_id == drug_id)
        
        if min_remainder is not None:
          q = q.where(status_retail_table.c.remainder >= min_remainder)
        
        if max_price is not None:
          q = q.where(status_retail_table.c.price <= max_price)
        
        return list(q.execute())

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
