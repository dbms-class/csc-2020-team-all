# encoding: UTF-8

## Веб сервер
import cherrypy
from connect import parse_cmd_line
from connect import create_connection_factory
from static import index

from peewee import *

@cherrypy.expose
class App(object):
  def __init__(self, args):
    #мне кажется так приятнее работать, но не знаю насколько это правильно
    self.connection_factory = create_connection_factory(args)

  @cherrypy.expose
  def index(self):
    return index()

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def update_retail(self, drug_id, pharmacy_id, remainder, price):
    #db = self.connection_factory.getconn()
    #try:
    #используем contextmanager, который сам в конце возращает сессию в пул
    with self.connection_factory.conn() as db: 
      cur = db.cursor()
      cur.execute(
        "SELECT * FROM Prices "
        "WHERE Pharmacy_id = %s AND Drug_id = %s",
        (pharmacy_id, drug_id)
      )

      if cur.fetchone() is not None:
        #если есть, то обновляем
        cur.execute(
          "UPDATE Prices "
          "SET PacksLeft = %s, Price = %s "
          "WHERE Pharmacy_id = %s AND Drug_id = %s",
          (remainder, price, pharmacy_id, drug_id)
        )
        key = 'update'
      else:
        # иначе вставляем
        cur.execute(
          "INSERT INTO Prices "
          "(Pharmacy_id, Drug_id, Price, PacksLeft) "
          "VALUES (%s, %s, %s, %s)",
          (pharmacy_id, drug_id, price, remainder)
        )
        key = 'insert'     

      #обязательный
      db.commit()
      return {key : 'ok'}
    #finally:
    #  self.connection_factory.putconn(db)
    
  @cherrypy.expose
  @cherrypy.tools.json_out()
  def update_retail_peewe(self, drug_id, pharmacy_id, remainder, price):
    #db = self.connection_factory.getconn()
    #try:
    with self.connection_factory.conn() as db:
      # ВАЖНО: НАЗВАНИЕ ТАБЛИЦЫ И ЕЕ ПОЛЯ НУЖНО ПИСАТЬ МАЛЕНЬКИМИ БУКВАМИ
      prices_table = Table('prices').bind(db)
      q = prices_table.select(
        prices_table.c.id
        ).where(
          prices_table.c.pharmacy_id == pharmacy_id,
          prices_table.c.drug_id == drug_id
          )
      
      if q.exists() > 0:
        # если есть, то обновляем
        prices_table.update(
          packsleft = remainder,
          price = price
          ).where(
            prices_table.c.pharmacy_id == pharmacy_id, 
            prices_table.c.drug_id == drug_id
          ).execute()
        # а можно ли как то так?
        # q.update(
        #   packsleft = remainder,
        #   price = price
        #   ).execute()
        key = 'update'
      else:
        # иначе вставляем
        prices_table.insert(
          pharmacy_id = pharmacy_id,
          drug_id = drug_id,
          price = price, 
          packsleft = remainder
        ).execute() 
        key = 'insert'     
      #необязательный????
      #db.commit()
      return {key : 'ok'}
    #finally:
    #  self.connection_factory.putconn(db)
    
      

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def drug(self):
    #db = self.connection_factory.getconn()
    #try:
    with self.connection_factory.conn() as db:
      cur = db.cursor()
      cur.execute("SELECT Id, Trade_Name, International_name FROM Drug")
      result = []
      drugs = cur.fetchall()
      for d in drugs:
        result.append({"id": d[0], "trade_name": d[1], "inn": d[2]})
      return result
    #finally:
    # self.connection_factory.putconn(db)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def drug_peewe(self):
    #db = self.connection_factory.getconn()
    #try:
    with self.connection_factory.conn() as db:
      drug_table = Table('drug').bind(db)
      d = drug_table.select(
        drug_table.c.id,
        drug_table.c.trade_name,
        drug_table.c.international_name
      )
      return list(d.execute())
    #finally:
    # self.connection_factory.putconn(db)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def pharmacy(self):
    #db = self.connection_factory.getconn()
    #try:
    with self.connection_factory.conn() as db:
      cur = db.cursor()
      cur.execute("SELECT * FROM Pharmacy")
      result = []
      pharmacies = cur.fetchall()
      for p in pharmacies:
        result.append({"id": p[0], "num": p[1], "address": p[2]})
      return result
    #finally:
    #  self.connection_factory.putconn(db)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def pharmacy_peewe(self):
    #db = self.connection_factory.getconn()
    #try:
    with self.connection_factory.conn() as db:
      pharmacy_table = Table('pharmacy').bind(db)
      # p = pharmacy_table.select() почему то не работает
      p = pharmacy_table.select(
        pharmacy_table.c.id,
        pharmacy_table.c.pharmacynumber,
        pharmacy_table.c.address
        )
      # Проблемы с кодировкой
      return list(p.execute())
    #finally:
    #  self.connection_factory.putconn(db)

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def status_retail(self, drug_id = None, min_remainder = None, max_price = None):
    with self.connection_factory.conn() as db:
      prices_table = Table('prices').bind(db)
      drug_table = Table('drug').bind(db)
      pharmacy_table = Table('pharmacy').bind(db)

      #можно сделать представление, но надо ли?
      drugs_min_max_price = prices_table.select(
        prices_table.c.drug_id,
        fn.MIN(prices_table.c.price).alias('min_price'),
        fn.MAX(prices_table.c.price).alias('max_price')
      ).group_by(prices_table.c.drug_id)

      #можно сделать представление
      q = prices_table.select(
        prices_table.c.drug_id,
        drug_table.c.trade_name,
        drug_table.c.international_name,
        prices_table.c.pharmacy_id,
        pharmacy_table.c.address,
        prices_table.c.packsleft,
        #какая то ошибка с Decimal
        #prices_table.c.price,
        #drugs_min_max_price.c.min_price,
        #drugs_min_max_price.c.max_price
      ).join(
        drug_table, on=(prices_table.c.drug_id == drug_table.c.id)
      ).join(
        pharmacy_table, on=(prices_table.c.pharmacy_id == pharmacy_table.c.id)
      ).join(
        drugs_min_max_price, on=(prices_table.c.drug_id == drugs_min_max_price.c.drug_id)
      )

      if drug_id is not None:
        q = q.where(prices_table.c.drug_id == drug_id)
      
      if min_remainder is not None:
        q = q.where(prices_table.c.packsleft >= min_remainder)
      
      if max_price is not None:
        q = q.where(prices_table.c.price <= max_price)

      return list(q.execute())


  @cherrypy.expose
  @cherrypy.tools.json_out()
  def status_retail_with_table_view(self, drug_id = None, min_remainder = None, max_price = None):
    with self.connection_factory.conn() as db:
      #prices_table = Table('prices').bind(db)
      status_retail_table = Table('status_retail').bind(db)
      
      q = status_retail_table.select(
        status_retail_table.c.drug_id,
        status_retail_table.c.drug_trade_name,
        status_retail_table.c.drug_inn,
        status_retail_table.c.pharmacy_id,
        status_retail_table.c.pharmacy_address,
        status_retail_table.c.regitmainder,
        #status_retail_table.c.price,
        #status_retail_table.c.min_price,
        #status_retail_table.c.max_price
      )
      # drugs_min_max_price.c.min_price,
      # drugs_min_max_price.c.max_price
      # ).join(
      #   drugs_min_max_price, on=
      #   (status_retail_table.c.drug_id == drugs_min_max_price.c.drug_id)
      # )

      if drug_id is not None:
        q = q.where(status_retail_table.c.drug_id == drug_id)
      
      if min_remainder is not None:
        q = q.where(status_retail_table.c.remainder >= min_remainder)
      
      if max_price is not None:
        q = q.where(status_retail_table.c.price <= max_price)
      
      return list(q.execute())
  
  @cherrypy.expose
  @cherrypy.tools.json_out()
  def drug_move(self,drug_id,min_remainder,target_income):
    with self.connection_factory.conn() as db:
      prices_table = Table('prices').bind(db)
      pharmacy_table = Table('pharmacy').bind(db)
    
      qmin = prices_table.select(
        fn.MIN(prices_table.c.price)
        ).where(
          prices_table.c.drug_id == drug_id,
          prices_table.c.packsleft >= min_remainder,
          ).scalar()

      
      qminid = prices_table.select(
        prices_table.c.pharmacy_id
        ).where(
          prices_table.c.drug_id == drug_id,
          prices_table.c.packsleft >= min_remainder,
          prices_table.c.price == qmin
          ).execute()


      qmax = prices_table.select(
        fn.MAX(prices_table.c.price)
        ).where(
          prices_table.c.drug_id == drug_id,
          prices_table.c.packsleft < min_remainder,
          ).scalar()

      
      qmaxid = prices_table.select(
        prices_table.c.pharmacy_id
        ).where(
          prices_table.c.drug_id == drug_id,
          prices_table.c.packsleft >= min_remainder,
          prices_table.c.price == qmax
          ).execute()

    
      return {
          "from_pharmacy_id": str(qminid), 
          "to_pharmacy_id": str(qmaxid), 
          "price_difference": float(qmax) - float(qmin), 
          "count": 20} 
    
    #https://csc-2020-team-all-2.dmitrybarashev.repl.co/drug_move?drug_id=1&min_remainder=1&target_income=1
      
      
      



if __name__ == '__main__':
  cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
  })
  cherrypy.quickstart(App(parse_cmd_line()))