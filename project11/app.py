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
    def volunteers(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Volunteers;")
            result = []
            commanders = cur.fetchall()
            for c in commanders:
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
            country_id = int(cur.fetchone()[0])
            volunteer_id = int(volunteer_id)
            if sportsman.isdigit():
                sportsman_id = int(sportsman)
                cur.execute("UPDATE sportsman SET country_id=%s, volunteer_id=%s WHERE id=%s;",
                            (country_id, volunteer_id, sportsman_id))
                status_message = 'UPDATED'
            else:
                cur.execute("INSERT INTO sportsman (name, country_id, volunteer_id) VALUES(%s, %s, %s);",
                            (sportsman, country_id, volunteer_id))
                status_message = 'INSERTED'
                return status_message
        finally:
            connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id=None, sportsman_count=0, total_task_count=0):
        db = connection_factory.getconn()
        sportsman_count = int(sportsman_count)
        total_task_count = int(total_task_count)
        try:
            cur = db.cursor()
            if volunteer_id is None:
                cur.execute(
                    "SELECT * FROM VolunteerLoad WHERE VolunteerLoad.sportsman_count >= %s AND VolunteerLoad.total_task_count>=%s;",
                    (sportsman_count, total_task_count))
            else:
                volunteer_id = int(volunteer_id)
                cur.execute(
                    "SELECT * FROM VolunteerLoad WHERE VolunteerLoad.sportsman_count >= %s AND VolunteerLoad.total_task_count>=%s AND VolunteerLoad.volunteer_id = %s;",
                    (sportsman_count, total_task_count, volunteer_id))
            result = []
            for f in cur.fetchall():
                result.append({
                    "volunteer_id": f[0],
                    "volunteer_name": f[1],
                    "sportsman_count": f[2],
                    "total_task_count": f[3],
                    "next_task_time": "" if f[4] is None else f[4].strftime("%m/%d/%Y, %H:%M:%S"),
                    "next_task_id": f[5]
                })
            return result
        finally:
            connection_factory.putconn(db)


# def volunteer_unassign(self, volunteer_id, task_ids):
#   db = connection_factory.getconn()
#   volunteer_id = int(volunteer_id)
#   try:
#     cur = db.cursor()
#     cur.execute("SELECT id,name FROM volunteers WHERE volunteers.id=%s",(volunteer_id)
#     quitter = Volunteer(cur.fetchone())
#     for task in quitter.tasks():
#       cur = db.cursor()
#       cur.execute("SELECT id,name FROM volunteers WHERE volunteers.id=%s",(volunteer_id)
  # if task_ids = '*':

  # else:


class Volunteer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def delegations(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(
                "SELECT DISTINCT delegation_id FROM sportsman WHERE volunteer_id=%s", (self.id,)
            )
            result = set()
            for f in cur.fetchall():
                result.add(tas[0])
            return result
        finally:
            connection_factory.putconn(db)

     def tasks(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(
                "SELECT id, date, time FROM volunteer_task WHERE volunteer_id=%s", (self.id,)
            )
            result = set()
            for f in cur.fetchall():
                result.add(Task(f[0], f[1], f[2]))
            return result
        finally:
            connection_factory.putconn(db)


def Task(self):
  def __init__(self, id, _date, _time):
    self.id = id
    self.date = _date
    self.time = _time
       

# volunteer_task,id, date, time
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
