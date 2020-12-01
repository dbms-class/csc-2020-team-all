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
        "SELECT PharmacyNumber FROM Prices "
        "WHERE PharmacyNumber = %s AND Drug_id = %s",
        (pharmacy_id, drug_id)
      )

      if cur.fetchone() is not None:
        #если есть, то обновляем
        cur.execute(
          "UPDATE Prices "
          "SET PacksLeft = %s, Price = %s "
          "WHERE PharmacyNumber = %s AND Drug_id = %s",
          (remainder, price, pharmacy_id, drug_id)
        )
        key = 'update'
      else:
        # иначе вставляем
        cur.execute(
          "INSERT INTO Prices "
          "(PharmacyNumber, Drug_id, Price, PacksLeft) "
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
        prices_table.c.pharmacynumber
        ).where(
          prices_table.c.pharmacynumber == pharmacy_id,
          prices_table.c.drug_id == drug_id
          )
      
      if q.exists() > 0:
        # если есть, то обновляем
        prices_table.update(
          packsleft = remainder,
          price = price
          ).where(
            prices_table.c.pharmacynumber == pharmacy_id, 
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
          pharmacynumber = pharmacy_id,
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
      cur.execute("SELECT Number, Address FROM Pharmacy")
      result = []
      pharmacies = cur.fetchall()
      for p in pharmacies:
        result.append({"id": p[0], "num": p[0], "address": p[1]})
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
      p = pharmacy_table.select(
        pharmacy_table.c.number,
        pharmacy_table.c.address
      )
      # Проблемы с кодировкой
      return list(p.execute())
          
if __name__ == '__main__':
  cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
  })
  cherrypy.quickstart(App(parse_cmd_line()))