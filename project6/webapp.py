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


    @cherrypy.expose
    def fill(self):
        script = ''
        with open('../project6/Project6.sql') as ddl:
            script = '\n'.join(list(map(str.rstrip, ddl.readlines())))
        if script == '':
            return 'Failed to read file'
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute(script)
        return 'Done'

    @cherrypy.expose
    def test_data(self):
      with create_connection(self.args) as db:
        cur = db.cursor()
        cur.execute(
          """
          INSERT INTO Countries(name) VALUES('Russia'),('USA');
          INSERT INTO Volonteers(name_volonteer) VALUES('vasya'),('petya');
          """
        )
      return 'Done'



    @cherrypy.expose
    @cherrypy.tools.json_out()
    def register(self, sportsman=None, country=None, volunteer_id=None):
      with create_connection(self.args) as db:
          cur = db.cursor()
          cur.execute(
            (
              f"""
              INSERT INTO Athlete(name_athlete, birthday, delegation_id, volonteer_id, home_facility) 
              VALUES({sportsman},{country}, {volunteer_id})
              """
            )
          )


    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
      with create_connection(self.args) as db:
          cur = db.cursor()
          cur.execute('SELECT id, name FROM Countries')
          result = []
          countries = cur.fetchall()
          for c in countries:
              result.append({"id": c[0], "name": c[1]})
          return result         


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
      with create_connection(self.args) as db:
          cur = db.cursor()
          cur.execute('SELECT id_volonteer, name_volonteer FROM Volonteers')
          result = []
          volonteers = cur.fetchall()
          for c in volonteers:
              result.append({"id": c[0], "name": c[1]})
          return result

         

  


    


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))