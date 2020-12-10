# encoding: UTF-8

## Веб сервер
import json
import cherrypy
import cherrypy_cors

from connect import parse_cmd_line
from connect import create_connection, connection_factory
from static  import index
from peewee import *

# класс для волонтеров
class Test:
  def __init__(self, name):
    self.name = name

  def get_name(self):
    return self.name


class Volunteers:
  def __init__(self, id, name, phone, task_id, start_datetime):
    self.id = id
    self.name = name
    self.phone = phone
    self.task_id = task_id
    self.start_datetime = start_datetime

  def get_id(self):
    return self.id

  def get_name(self):
    return self.name

  def get_phone(self):
    return self.phone

  def get_task_id(self):
    return self.task_id

  def get_start_datetime(self):
    return self.start_datetime


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
    @cherrypy.tools.json_out()
    def planets(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Planet P")
            result = []
            planets = cur.fetchall()
            for p in planets:
                result.append({"id": p[0], "name": p[1]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def sportsman(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT id, name, country_id, volunteer_id  FROM Sportsmens")
          result = []
          commanders = cur.fetchall()
          for c in commanders:
              result.append({"id": c[0], "name": c[1], "counry_id":c[2], "volunteer_id":c[3]})
          return result
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * FROM Countries;")
          result = []
          commanders = cur.fetchall()
          for c in commanders:
            result.append({"id": c[0], "name": c[1]})
          return result
        finally:
          connection_factory.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def tasks(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * FROM Task;")
          result = []
          commanders = cur.fetchall()
          for c in commanders:
            result.append({"id": c[0], "name": c[1]})
          return result
        finally:
          connection_factory.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add_test(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("CREATE TABLE Test1(id    serial PRIMARY key, login varchar(40)     NOT NULL, pass varchar(40)     NOT NULL, x FLOAT(8) not NULL, y FLOAT(8) not NULL);CREATE TABLE Test2(id    serial PRIMARY key,x FLOAT(8) not NULL,y FLOAT(8) not NULL);INSERT INTO test1 (login, pass, x, y) VALUES('1', '1', 45.0530611, 39.0278447), ('2', '2', 45.0566486, 38.9929379);INSERT INTO test2 (x, y) VALUES(45, 39), (45.0499015, 38.9284980);")
          db.commit()
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_test(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * FROM Test1;")
          result = ''
          commanders = cur.fetchall()
          for c in commanders:
            #result.append({"id": c[0], "x": c[3], "y": c[4]})
            result += str(c[0])+'|'+str(c[3])+"|"+str(c[4])+'*'
          result = result[:-1]
          return result
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_test2(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * FROM Test2;")
          result = ''
          commanders = cur.fetchall()
          for c in commanders:
            #result.append({"id": c[0], "x": c[1], "y": c[2]})
            result += str(c[0])+'|'+str(c[1])+"|"+str(c[2])+'*'
          result = result[:-1]
          return result
        finally:
          connection_factory.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_log(self, log, p):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * from test1 WHERE login ='"+log+"' and pass = '"+p+"'")
          commanders = cur.fetchall()
          if len(commanders)==1:
            return commanders[0][0]
          else:
            return False
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_reg(self, log, p, x, y):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT * from test1 WHERE login ='"+log+"'")
          commanders = cur.fetchall()
          if len(commanders)!=0:
            return False

          query = f'''
        INSERT INTO test1 (login, pass, x, y) VALUES({log}, {p}, {x}, {y})
    '''
          cur.execute(query)
          db.commit()
          return True
        finally:
          connection_factory.putconn(db)
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_set_loc(self, id, x, y):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()

          query = f'''
        UPDATE  test1 set x={x}, y={y} WHERE id = {id};
        '''
          cur.execute(query)
          db.commit()
          return True
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_del_user(self, id):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()

          query = f'''
        DELETE from test1 WHERE id = {id};
        '''
          cur.execute(query)
          db.commit()
          return True
        finally:
          connection_factory.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_add_target(self, x, y):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()

          query = f'''
        INSERT INTO test2 (x, y) VALUES({x}, {y})
        '''
          cur.execute(query)
          db.commit()
          return True
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def test_del_target(self, id):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()

          query = f'''
        DELETE from test2 WHERE id = {id};
        '''
          cur.execute(query)
          db.commit()
          return True
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add_tasks(self):
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("INSERT INTO Task (volunteer_id, start_datetime, text) VALUES (1,'2020-11-19 12:00', 'a'), (2,'2020-11-19 13:00', 'b'), (1,'2020-11-19 14:00', 'c')")
          db.commit()
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
        db = connection_factory.getconn()
        try:
              cur = db.cursor()
              cur.execute("SELECT * FROM Volunteers;")
              result = []
              volunteers = cur.fetchall()
              for c in volunteers:
                  result.append({"id": c[0], "name": c[1]})
              return result
        finally:
          connection_factory.putconn(db)



    @cherrypy.expose
    @cherrypy.tools.json_out()
    def Test(self, mes):
        db = connection_factory.getconn()
        try:
              return 'result: ' + mes
        finally:
          connection_factory.putconn(db)  

# получение волонтеров через пиви
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def new_volunteers(self):
        db = connection_factory.getconn()
        try:
            volunteers = Table('volunteers').bind(db)
            v= volunteers.select(volunteers.c.name)
            v = v.objects(Test)
            result = []
            for c in v:
                  result.append({"name": c.get_name()})
            return result
        finally:
          connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def add_volunteers(self):
        db = connection_factory.getconn()
        try:
              cur = db.cursor()
              cur.execute("INSERT INTO Volunteers VALUES (3,'a', '34'), (4,'b', '43')")
              cur.execute("SELECT * FROM Volunteers;")
              result = []
              db.commit()
              volunteers = cur.fetchall()
              for c in volunteers:
                  result.append({"id": c[0], "name": c[1]})
              return result

        finally:
          connection_factory.putconn(db)




    @cherrypy.expose
    def register(self, sportsman, country, volunteer_id):
        status_message = 'SUCCESS'
        db = connection_factory.getconn()
        try:
          cur = db.cursor()
          cur.execute("SELECT id FROM Countries WHERE Countries.name=%s;", (country,))
          country_id, volunteer_id = int(cur.fetchone()[0]), int(volunteer_id)
          if sportsman.isdigit():
            sportsman_id = int(sportsman)
            cur.execute("UPDATE Sportsmens SET country_id=%s, volunteer_id=%s WHERE id=%s;", (country_id, volunteer_id, sportsman_id))
          else:
            cur.execute("INSERT INTO Sportsmens(name, gender, country_id, object_id, volunteer_id) VALUES(%s, %s, %s, 1, %s);", (sportsman, 'm', country_id, volunteer_id))  
        except Exception as e:
          status_message = f"Error: {e}"
        finally:
          connection_factory.putconn(db)
        return status_message


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id = None, sportsman_count = None, total_task_count = None):
        db = connection_factory.getconn()
        try:
            tab_task = Table('task').bind(db)
            tab_volunteers = Table('volunteers').bind(db)
            tab_sportsmens = Table('sportsmens').bind(db)

            result = []

            v = tab_volunteers.select(tab_volunteers.c.id,
                                      tab_volunteers.c.name, 
                                      tab_volunteers.c.phone, 
                                      tab_task.c.id.alias('task_id'), 
                                      tab_task.c.start_datetime
                                  ).join(tab_task, 
                                    on=(tab_volunteers.c.id == tab_task.c.volunteer_id)).distinct()
            # Есть повторы в выходном json
            # Например:
            # curl https://csc-2020-team-all-16.dmitrybarashev.repl.co/volunteer_load?sportsman_count=1\&total_task_count=2
            # [{"volunteer_id": 1, "volunteer_name": "Ricardo Milos", "sportsman_count": 1, "total_task_count": 2, "next_task_id": 3, "next_task_time": "2020-11-19 14:00:00"}, {"volunteer_id": 1, "volunteer_name": "Ricardo Milos", "sportsman_count": 1, "total_task_count": 2, "next_task_id": 1, "next_task_time": "2020-11-19 12:00:00"}]
            # 
            for c in v.objects(Volunteers):
                  current_volunteer_id = c.get_id()
                  result_sportsman_count = tab_sportsmens.select().where(tab_sportsmens.c.volunteer_id == current_volunteer_id).count()
                  result_total_task_count = tab_task.select().where(tab_task.c.volunteer_id == current_volunteer_id).count()
                  volunteer_name = c.get_name()
                  next_task_id = c.get_task_id()
                  next_task_time = c.get_start_datetime()

                  result_json = {
                        "volunteer_id": c.get_id(), 
                        "volunteer_name": c.get_name(), 
                        "sportsman_count": result_sportsman_count,
                        "total_task_count": result_total_task_count,
                        "next_task_id": next_task_id,
                        "next_task_time": str(next_task_time),
                  }

                  if sportsman_count is None and total_task_count is None:
                    if volunteer_id is None:
                      result.append(result_json)
                    else:
                      if current_volunteer_id == int(volunteer_id):
                        result.append(result_json)
                        break

                  if sportsman_count is not None and total_task_count is None:
                    if volunteer_id is None:
                        if result_sportsman_count >= int(sportsman_count):
                          result.append(result_json)
                    else:
                        if current_volunteer_id == int(volunteer_id):
                          if result_sportsman_count >= int(sportsman_count):
                            result.append(result_json)
                          break

                  if sportsman_count is None and total_task_count is not None:
                    if volunteer_id is None:
                      if result_total_task_count >= int(total_task_count):
                          result.append(result_json)
                    else:
                      if current_volunteer_id == int(volunteer_id):
                        if result_total_task_count >= int(total_task_count):
                          result.append(result_json)
                        break

                  if sportsman_count is not None and total_task_count is not None:
                    if volunteer_id is None:
                      if result_total_task_count >= int(total_task_count) and result_sportsman_count >= int(sportsman_count):
                          result.append(result_json)
                    else:
                      if current_volunteer_id == int(volunteer_id):
                        if result_total_task_count >= int(total_task_count) and result_sportsman_count >= int(sportsman_count):
                          result.append(result_json)
                        break

            #"volunteer_id": 1,
            #"volunteer_name": "Pedro",
            #"sportsman_count": 20,
            #"total_task_count": 3, // общее количество задач
            #"next_task_id": 146, // id ближайшей задачи  к now 
            #"next_task_time": "2020-11-19 12:00" // время ближайшей задачи

            return result
        finally:
          connection_factory.putconn(db)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_unassign(self, volunteer_id = None, sportsman_count = None, total_task_count = None):
        if (not volunteer_id.isnumeric()):
            return
        if (not platform.isnumeric()):
            return
        db = connection_factory.getconn()
        try:
            result = []
            return result
        finally:
          connection_factory.putconn(db)

  

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
