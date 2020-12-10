import cherrypy
import cherrypy_cors

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
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def apartments(self, country_id=None):
        with self.connection_factory.conn() as db:
          apartments = Table('apartments').bind(db)

          query = apartments.select(
            apartments.c.id,
            apartments.c.name,
            apartments.c.address,
            apartments.c.country_id
          )

          if country_id is not None:
            query = query.where(apartments.c.country_id == country_id)

          result = list(query)
          return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        with self.connection_factory.conn() as db:
          countries = Table('countries').bind(db)

          query = countries.select(
            countries.c.id,
            countries.c.name
          )

          result = list(query)
          return result

    def _update_price(self, db, apartment_id, week, price):
        prices = Table('prices').bind(db)
        query = prices.select(
          prices.c.price
        ).where(
          prices.c.apartment_id == apartment_id,
          prices.c.week == week
        )

        if query.exists():
          status = 'updated'
          query = prices.update(
            price = price
          ).where(
            prices.c.apartment_id == apartment_id,
            prices.c.week == week
          )
        else:
          status = 'inserted'
          query = prices.insert(
            apartment_id=apartment_id,
            week=week,
            price=price
          )

        query.execute()
        return {'status': status}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update_price(self, apartment_id, week, price):
        with self.connection_factory.conn() as db:
          return self._update_price(db, apartment_id, week, price)
  
    
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
          ).join(
            prices, on=(apartments.c.id == prices.c.apartment_id)
          ).where(
            apartments.c.country_id == country_id,
            prices.c.week == week
          )

          if max_price is not None:
              query = query.where(prices.c.price <= max_price)
          if bed_count is not None:
              query = query.where(apartments.c.bed_count >= bed_count)
          
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
      """
      Автоматическое применение скидок на жильё:
      * величина скидки фиксированная - 50 талеров
      * по всему свободному в данную неделю жилью считается средняя стоимость
      * без скидки вероятность сдать жильё - 0.5
      * если после скидки стоимость стала выше средней - вероятность становится 0.7
      * если после скидки стоимость стала ниже средней - вероятность становится 0.9
      * прибыль от применения скидки: (x - 50) * p - x * 0.5,
      *    где x - старая цена, p - вероятность (0.7 или 0.9)
      * хотим изменить цену в минимальном числе объектов, чтобы достичь прибыли target_plus
      * применяем скидку для выбранных объектов
      """
      with self.connection_factory.conn() as db:
          apartments = Table('availableapartmentprices').bind(db)

          # ищем среднюю цену
          average_price = apartments.select(
            fn.AVG(apartments.c.price)
          ).where(
            apartments.c.week == week,
            fn.COALESCE(apartments.c.start_week, 1) <= week,
            fn.COALESCE(apartments.c.end_week, 53) >= week,
            apartments.c.available
          ).scalar()

          # Запрос query вернет апартаменты, отсортированные в интересующем нас порядке: перый тот, который принесет больше дополнительной выручки.
          # Выражение case соответствует
          # CASE 
          # WHEN price  <AVG THEN (price-50)*0.9
          # ELSE (price-50)*0.7
          # END
          # Из ожидаемой стоимости со скидкой  надо вычесть ожидаемую без скидки, чтоб получить ожидаемый лишний доход.
          case = Case(None,[((apartments.c.price - 50) < average_price, 0.9 * (apartments.c.price - 50))], 0.7 * (apartments.c.price - 50)) - 0.5 * apartments.c.price

          query = apartments.select(
            apartments.c.id,
            apartments.c.price,
            case.alias('revenue')
          ).where(
            apartments.c.owner_id == owner_id,
            apartments.c.week == week,
            fn.COALESCE(apartments.c.start_week, 1) <= week,
            fn.COALESCE(apartments.c.end_week, 53) >= week,
            apartments.c.available
          ).order_by(
            case.desc()
          )

          # Сохраняем список объектов, для которых нужно применить скидку.
          # Останавливаемся, если достигли target_plus или подходящие объекты закончились.
          # Применяем скидку для выбранных объектов.
          expected_income = 0
          discounts = []
          for row in query:
            revenue = row['revenue']
            if revenue <= 0 or expected_income >= float(target_plus):
              break
            expected_income += revenue
            discounts.append(row)
            self._update_price(db, row['id'], week, row['price'] - 50)
          
          return list(map(lambda row: {
              "id": row['id'],
              "old_price": row['price'],
              "new_price": row['price'] - 50,
              "expected_income": float(row['revenue'])
          }, discounts))
          

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
