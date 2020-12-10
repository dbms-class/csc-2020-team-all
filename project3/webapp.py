# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import parse_cmd_line
from connect import connection_factory, txn
from static import index
from peewee import *

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
        def work(db, apartment_id, week, price):
          t = Table('price').bind(db)
          rowcount = t.update(price=price).where((t.c.apartment_id == apartment_id) & (t.c.week == week)).execute()
          if rowcount > 0:
              return True

          new_id = t.insert(apartment_id=apartment_id, week=week, price=price).execute()
          return new_id is not None
        
        return txn(lambda db: work(db, apartment_id=apartment_id, week=week, price=price))


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
      db = connection_factory.getconn()
      try:
        CountryView = Table('country').bind(db)
        q = CountryView.select(CountryView.c.id, CountryView.c.name)
        return [p for p in q]
      finally:
        connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def apartments(self, country_id=None):
      db = connection_factory.getconn()
      try:
        ApartmentView = Table('apartment').bind(db)
        q = ApartmentView.select(ApartmentView.c.id,
              ApartmentView.c.name,
              ApartmentView.c.country_id,
              ApartmentView.c.address
        )
        if country_id is not None:
          q = q.where(ApartmentView.c.country_id == country_id)
        return [p for p in q]
      finally:
        connection_factory.putconn(db)
 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_price(self, country_id, week, max_price=None, bed_count=None):
      db = connection_factory.getconn()
      try:
        ApartmentPriceView = Table('apartment_price_view').bind(db)
        q = ApartmentPriceView.select(ApartmentPriceView.c.id, ApartmentPriceView.c.name, ApartmentPriceView.c.country_id, ApartmentPriceView.c.num_of_bed, ApartmentPriceView.c.week, ApartmentPriceView.c.price) \
        .where((ApartmentPriceView.c.country_id == country_id) & (ApartmentPriceView.c.week == week))

        if max_price is not None:
          q = q.where(ApartmentPriceView.c.price <= max_price)
        
        if bed_count is not None:
          q = q.where(ApartmentPriceView.c.num_of_bed >= bed_count)
        
        return [p for p in q]
      finally:
        connection_factory.putconn(db)
  

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def appt_sale(self, landlord_id, week, target_plus):
      def to_json(row):
        return {"apartment_id": row[0], "landlord_id": row[1], "price": row[2], "week": row[3]}

      def get_fail_message():
        return {'Verdict': 'Target plus is not reachable'}

      def find_min_length_prefix(profit_list, target_plus):
        prefix_sum_target = 0
        for i, apartment in enumerate(profit_list):
          prefix_sum_target += apartment[1]
          if prefix_sum_target >= target_plus:
            return profit_list[:(i + 1)]
        return []

      with create_connection(self.args) as db:
          cur = db.cursor()
          cur.execute('SELECT AVG(price) FROM LANDLORD_UNRENTED_APARTMENTS WHERE week=%s GROUP BY week', week)
          weekly_mean_price = cur.fetchall()

          if not weekly_mean_price:
            return get_fail_message()

          weekly_mean_price = weekly_mean_price[0]

          cur.execute('SELECT * FROM LANDLORD_UNRENTED_APARTMENTS WHERE week=%s AND landlord_id=%s', 
            (week, landlord_id))
          landlord_unrented_apartments = [to_json(row) for row in cur.fetchall()]

          base_profit_expectation = 0
          apartment_profit_list = []
          for apartment in landlord_unrented_apartments:
            base_profit_expectation += 0.5 * apartment['price']
            shifted_price = max(apartment['price'] - 50, 0)
            apartment.update({'new_price': shifted_price})
            new_prob = 0.9 if shifted_price < weekly_mean_price else 0.7
            apartment_profit_diff = new_prob * shifted_price - 0.5 * apartment['price']
            apartment.update({"profit_diff": apartment_profit_diff})
            apartment_profit_list.append((apartment['apartment_id'], apartment_profit_diff))
          
          apartment_profit_list.sort(key=lambda x: x[1], reverse=True)

          min_apartment_list = find_min_length_prefix(apartment_profit_list, target_plus)

          if not min_apartment_list:
            return get_fail_message()

          result = []
          for apartment in landlord_unrented_apartments:
            if apartment['apartment_id'] in min_apartment_list:
              result.append(
                            {
                              "apartment_id": apartment['apartment_id'], 
                              "old_price": apartment['price'],
                              "new_price": apartment['new_price'],
                              "expected_income": apartment['profit_diff']
                            }
                          )
          return result
              

            
              

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



cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))

