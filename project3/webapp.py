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
    '''
    database enuanake contains
    table APARTMENT:

    id	name	landlord_id	country_id	
    1	MorningPlace	2	3							
    2	Kalina	1	1

    table COUNTRY:

    id	name	commission
    1	Russia	
    2	UK	
    3	US
    '''

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
            #result = []
            # planets = cur.fetchall()
            # for p in planets:
            #     result.append({"id": p[0], "name": p[1]})
            return "UPDATE DONE"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute('SELECT id, name FROM COUNTRY')
            result = []
            countries = cur.fetchall()
            for c in countries:
                result.append({"id": c[0], "name": c[1]})
            return result  


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def apartments(self, country_id=None):
       with create_connection(self.args) as db:
            if country_id is None:
              cur = db.cursor()
              cur.execute('SELECT id, name, country_id, address FROM APARTMENT')
              result = []
              apartments = cur.fetchall()
              for c in apartments:
                  result.append({"id": c[0], "name": c[1], "address" : c[3], "country_id" : c[2]})
              return result 
            else:
              cur = db.cursor()
              cur.execute('SELECT id, name, country_id, address FROM APARTMENT WHERE country_id =%s' %(country_id))
              result = []
              apartments = cur.fetchall()
              for c in apartments:
                  result.append({"id": c[0], "name": c[1], "address" : c[3], "country_id" : c[2]})
              return result 

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_price(self, country_id, week, max_price=None, bed_count=None):
       with create_connection(self.args) as db:
            cur = db.cursor()
            
            if max_price is None and bed_count is None:
              cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s' %(week, country_id))
            if max_price is None and bed_count is not None:
              cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s and num_of_bed = %s' %(week, country_id, bed_count))
            if max_price is not None and bed_count is None:
              cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s and price <= %s' %(week, country_id, max_price))
            if max_price is not None and bed_count is not None:
              cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s and price <= %s and num_of_bed = %s' %(week, country_id, max_price, bed_count))
            result = []
            apartments = cur.fetchall()
            for c in apartments:
                result.append({"apartment_id": c[0], "apartment_name": c[1], "bed_count" : c[3], "week" : c[4], "price" :c[5], "max_price": max_price, "min_price" : 0})
            return result 
            
            # if max_price is None and bed_count is None:
            #   cur = db.cursor()
            #   cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s' %(week, country_id))
            #   result = []
            #   apartments = cur.fetchall()
            #   for c in apartments:
            #       result.append({"apartment_id": c[0], "apartment_name": c[1], "bed_count" : c[3], "week" : c[4], "price" :c[5], "max_price": max_price, "min_price" : 0})
            #   return result 
            # if max_price is None and bed_count is not None:
            #   cur = db.cursor()
            #   cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s and num_of_bed = %s' %(week, country_id, bed_count))
            #   result = []
            #   apartments = cur.fetchall()
            #   for c in apartments:
            #       result.append({"apartment_id": c[0], "apartment_name": c[1], "bed_count" : c[3], "week" : c[4], "price" :c[5], "max_price": max_price, "min_price" : 0})
            #   return result 
            # if max_price is not None and bed_count is None:
            #   cur = db.cursor()
            #   cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s and price <= %s' %(week, country_id, max_price))
            #   result = []
            #   apartments = cur.fetchall()
            #   for c in apartments:
            #       result.append({"apartment_id": c[0], "apartment_name": c[1], "bed_count" : c[3], "week" : c[4], "price" :c[5], "max_price": max_price, "min_price" : 0})
            #   return result 
            # if max_price is not None and bed_count is not None:
            #   cur = db.cursor()
            #   cur.execute('SELECT * FROM APARTMENT_PRICE_VIEW WHERE week = %s AND country_id = %s and price <= %s and num_of_bed = %s' %(week, country_id, max_price, bed_count))
            #   result = []
            #   apartments = cur.fetchall()
            #   for c in apartments:
            #       result.append({"apartment_id": c[0], "apartment_name": c[1], "bed_count" : c[3], "week" : c[4], "price" :c[5], "max_price": max_price, "min_price" : 0})
            #   return result 

              

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

