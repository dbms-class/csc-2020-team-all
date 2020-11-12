# encoding: UTF-8

## Веб сервер
import json
import cherrypy
import cherrypy_cors

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
    def commanders(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Commander")
            result = []
            commanders = cur.fetchall()
            for c in commanders:
                result.append({"id": c[0], "name": c[1]})
            return result
  
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM Countries;")
            result = []
            commanders = cur.fetchall()
            for c in commanders:
                result.append({"id": c[0], "name": c[1]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Volunteers;")
            result = []
            commanders = cur.fetchall()
            for c in commanders:
                result.append({"id": c[0], "name": c[1]})
            return result

    @cherrypy.expose
    def register(self, sportsman, country, volunteer_id):
        status_message = 'SUCCESS'
        try:
          with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id FROM Countries WHERE Countries.name=%s;", (country,))
            country_id, volunteer_id = int(cur.fetchone()[0]), int(volunteer_id)
            if sportsman.isdigit():
              sportsman_id = int(sportsman)
              cur.execute("UPDATE Sportsmens SET country_id=%s, volunteer_id=%s WHERE id=%s;", (country_id, volunteer_id, sportsman_id))
            else:
              cur.execute("INSERT INTO Sportsmens(name, gender, country_id, object_id, volunteer_id) VALUES(%s, %s, %s, 1, %s);",
              			 (sportsman, 'm', country_id, volunteer_id))
        except Exception as e:
          status_message = f"Error: {e}"
        return status_message

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
