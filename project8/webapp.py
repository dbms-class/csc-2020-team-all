# encoding: UTF-8

## Веб сервер
import cherrypy
import cherrypy_cors

from connect import parse_cmd_line
from connect import create_connection_factory
from static import index

from peewee import *


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
    def drop(self, table):
        with self.connection_factory.conn() as db:
            cur = db.cursor()
            cur.execute(f'DROP TABLE {table}')
        return 'Done'

    @cherrypy.expose
    def fill(self):
        script = ''
        with open('../project8/project8.sql') as ddl:
            script = '\n'.join(list(map(str.rstrip, ddl.readlines())))
        if script == '':
            return 'Failed to read file'
        with self.connection_factory.conn() as db:
            cur = db.cursor()
            cur.execute(script)
        return 'Done'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def apartments(self, country_id=None):
        with self.connection_factory.conn() as db:
          cur = db.cursor()
          query = f'SELECT id, name, address, country_id FROM Apartments'
          if country_id is not None:
              query += f' WHERE country_id = {country_id}'
          cur.execute(query)

          return list(map(
              lambda apartment: {
                  'id': apartment[0], 'name': apartment[1],
                  'address': apartment[2], 'country_id': apartment[3]
              },
              cur.fetchall()
          ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        with self.connection_factory.conn() as db:
          cur = db.cursor()
          query = 'SELECT id, name FROM Countries'
          cur.execute(query)
          return list(map(
              lambda country: {'id': country[0], 'name': country[1]},
              cur.fetchall()
          ))


    @cherrypy.expose
    def update_price(self, apartment_id, week, price):
        with self.connection_factory.conn() as db:
          cur = db.cursor()
          query = f'UPDATE Prices SET price = {price} WHERE apartment_id = {apartment_id} and week = {week}'
          cur.execute(query)
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_price(self, country_id, week, max_price=None, bed_count=None):
        with self.connection_factory.conn() as db:
          apartments = Table('apartments').bind(db)
          prices = Table('prices').bind(db)
          query = apartments.select(
            apartments.c.id,
            apartments.c.name,
            apartments.c.bed_count,
            prices.c.week,
            prices.c.price
          ).join(prices,
              on=(apartments.c.id == prices.c.apartment_id)
          ).where((apartments.c.country_id == country_id)&(prices.c.week == week))

          if max_price is not None:
              query = query.where(price <= max_price)
          if bed_count is not None:
              query = query.where(bed_count >= bed_count)
          
          query = query.namedtuples()
          
          prices = [row.price for row in query]
          min_p, max_p = min(prices, default=0), max(prices, default=0)
          return list(map(
              lambda apartment: {
                  'id': apartment.id, 
                  'name': apartment.name,
                  'bed_count': apartment.bed_count,
                  'week': apartment.week,
                  'price': apartment.price,
                  'min_price': min_p,
                  'max_price': max_p
              },
              query
          ))
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def appt_sale(self, owner_id, week, target_plus):
      with self.connection_factory.conn() as db:
          apartments = Table('apartments').bind(db)
          applications = Table('applications').bind(db)
          prices = Table('prices').bind(db)
          apartments_booked  = apartments.select(
            apartment.c.id,
            applications.c.end_date.week.alias('end_week'),
            applications.c.start_date.week.alias('start_week')
          ).join(apartaments, 
                  on=(apartments.c.id == applications.c.apartment_id))
          query = apartments.select(
            prices.c.week,
            prices.c.price
          ).join(prices,
              on=(apartments.c.id == prices.c.apartment_id)
          ).join(apartments_booked,
              on=(apartments.c.id == applications.c.apartment_id)
          ).where((apartments.c.owner_id == owner_id) &
          (week >= apartments_booked.start_week) & 
          (week <= apartments_booked.end_week))
          # TODO: Посчитать результат с коэффициентами

def run():
    cherrypy_cors.install()
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
    })
    config = {
        '/': {
            'cors.expose.on': True,
        },
    }
    cherrypy.quickstart(App(parse_cmd_line()), config=config)


if __name__ == '__main__':
    run()
