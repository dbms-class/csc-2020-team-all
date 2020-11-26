# encoding: UTF-8

## Веб сервер
import json
import cherrypy
import cherrypy_cors

from connect import parse_cmd_line
from connect import create_connection, connection_factory
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
        with create_connection(self.args) as db:
          # db = connection_factory.getconn()
          try:
            cur = db.cursor()
            cur.execute("SELECT id FROM Countries WHERE Countries.name=%s;", (country,))
            country_id = int(cur.fetchone()[0])
            volunteer_id = int(volunteer_id)
            if sportsman.isdigit():
              sportsman_id = int(sportsman)
              cur.execute("UPDATE sportsman SET country_id=%s, volunteer_id=%s WHERE id=%s;", (country_id, volunteer_id, sportsman_id))
              status_message = 'UPDATED'
            else:
              cur.execute("INSERT INTO sportsman (name, country_id, volunteer_id) VALUES(%s, %s, %s);", (sportsman, country_id, volunteer_id))
              status_message = 'INSERTED'
          finally:
            pass
            # connection_factory.putconn(db)
        return status_message

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id=, sportsman_count, total_task_count):
      pass
    
      # query = []
      # if (volunteer_id):
      #   query.append("volunteer_id=%s")
      #   Valunteer -> Sportsmens
      #   Valunterr -> Task
      #   Aggr(first, second):
      #   [
      #     {
      #     ”volunteer_id”: 1,
      #     ”volunteer_name”: ”Pedro”,
      #     ”sportsman_count”: 20,
      #     ”total_task_count”: 3, // общее количество задач
      #     ”next_task_id”: 146, // id ближайшей задачи к now
      #     ”next_task_time”: ”2020-11-19 12:00” // время ближайшей задачи
      #     },
      #     ...
      #   ]


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