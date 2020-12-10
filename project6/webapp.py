# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import parse_cmd_line
from connect import connection_factory
from static import index
from peewee import *
import json

import logging


class VolunteerLoad:
  def __init__(self, id_volonteer, name_volonteer, sportsman_count, total_task_count, next_task_id, next_task_time):
    self.volunteer_id = id_volonteer,
    self.volunteer_name = name_volonteer,
    self.sportsman_count = sportsman_count,
    self.total_task_count = total_task_count,
    self.next_task_id = next_task_id,
    self.next_task_time = next_task_time
    

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


    @cherrypy.expose
    def fill(self):
        script = ''
        with open('../project6/Project6.sql') as ddl:
            script = '\n'.join(list(map(str.rstrip, ddl.readlines())))
        if script == '':
            return 'Failed to read file'
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(script)
        finally:
          connection_factory.putconn(db)
        return 'Done'

    @cherrypy.expose
    def test_data(self):
      db = connection_factory.getconn()
      try:
        cur = db.cursor()
        cur.execute(
          """
          INSERT INTO Countries(country) VALUES('Russia'),('USA');
          INSERT INTO Volonteers(name_volonteer) VALUES('vasya'),('petya');
          """
        )
      finally:
          connection_factory.putconn(db)
      return 'Done'



    @cherrypy.expose
    @cherrypy.tools.json_out()
    def register(self, sportsman=None, country=None, volunteer_id=None):
      db = connection_factory.getconn()
      try:
          cur = db.cursor()
          cur.execute("SELECT D.id_delegation FROM Delegation D JOIN Countries C on D.id_country = C.id_country where C.county = %s", str(country))

          country_delegation = cur.fetchone()
          if country_delegation is None:
            raise cherrypy.HTTPError(400, f"There is no delegation for country {country}")
            
          cur.execute(
            (
              """
              INSERT INTO Athlete(name_athlete, delegation_id, volonteer_id) 
              VALUES(%s, %s, %s)
              """,
              sportsman, country_delegation[0], volunteer_id
            )
          )
          return {"sportsman": sportsman, "county": country, "volunteer_id": volunteer_id}
      finally:
        connection_factory.putconn(db)


    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
      db = connection_factory.getconn()
      try:
          cur = db.cursor()
          cur.execute('SELECT id, name FROM Countries')
          result = []
          countries = cur.fetchall()
          for c in countries:
              result.append({"id": c[0], "name": c[1]})
          return result      
      finally:
        connection_factory.putconn(db)   


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
      db = connection_factory.getconn()
      try:
        cur = db.cursor()
        cur.execute('SELECT id_volonteer, name_volonteer FROM Volonteers')
        result = []
        volonteers = cur.fetchall()
        for c in volonteers:
            result.append({"id": c[0], "name": c[1]})
        return result
      finally:
        connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id=None, sportsman_count=None, total_task_count=None):

      logger = logging.getLogger('peewee')
      logger.addHandler(logging.StreamHandler())
      logger.setLevel(logging.DEBUG)

      db = connection_factory.getconn()
      try:
        table = Table('volonteers_load').bind(db)
        q = table.select(
          table.c.id_volonteer,
          table.c.name_volonteer,
          table.c.sportsman_count,
          table.c.total_task_count,
          table.c.next_task_id,
          table.c.next_task_time
          )
        if volunteer_id is not None:
          q = q.where(table.c.volonteer_id == volunteer_id)
        if sportsman_count is not None:
          q = q.where(table.c.sportsmen_count >= sportsman_count)
        if total_task_count is not None:
          q = q.where(table.c.total_task_count >= total_task_count)
        
        

        def to_json(f):
            base ={
              "volunteer_name": f.volunteer_name[0],
              "next_task_id": f.next_task_id[0], # id ближайшей задачи к now
              "next_task_time": f.next_task_time # время ближайшей задачи
            }
            if volunteer_id is not None:
                base.update({"volunteer_id": f.volunteer_id})
            if sportsman_count is not None:
                base.update({"sportsman_count": f.sportsman_count})
            if total_task_count is not None:
                base.update({"total_task_count": f.total_task_count})
            return base
  

        q = q.objects(VolunteerLoad)
        return list(map(to_json,q))
        return [f.__dict__ for f in q]
      finally:
        connection_factory.putconn(db)

    @cherrypy.expose 
    @cherrypy.tools.json_out()
    def volunteer_unassign(self, volunteer_id, task_ids):
      pass
         

  




cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))