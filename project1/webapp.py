# encoding: UTF-8

## Веб сервер
import cherrypy
import cherrypy_cors
import re

from connect import parse_cmd_line
from connect import create_connection
from static import index

DIGITS_RE = re.compile('\d+')

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
            cur.execute("SELECT id, name FROM Countries")
            countries = cur.fetchall()
            return [{"id": c[0], "name": c[1]} for c in countries]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM volunteers;")
            volunteers = cur.fetchall()
            return [{"id": v[0], "name": v[1]} for v in volunteers]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def register(self, sportsman, country, volunteer_id):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM Countries_delegation WHERE country_name = %s", (str(country),))
            delegation = cur.fetchone()
            if delegation is None:
                raise cherrypy.HTTPError(404, "There is no delegation for country " + country)
# http://csc-2020-team-all-1.dmitrybarashev.repl.co/register?country=Country1&sportsman=asd&volunteer_id=1
            cur.execute("SELECT * FROM Volunteers WHERE id = %s", (int(volunteer_id),))
            volunteer = cur.fetchone()
            if volunteer is None:
                raise cherrypy.HTTPError(404, "There is no volunteer id=" + volunteer_id)

            if DIGITS_RE.match(sportsman) != None:
                cur.execute(
                  "UPDATE Athletes SET delegation_id = %s, volunteer_id = %s WHERE id = %s", 
                  (delegation[0], int(volunteer_id), sportsman))
            else:
                cur.execute(
                    "INSERT INTO Athletes (name, delegation_id, volunteer_id) values (%s, %s, %s)",
                    (sportsman, delegation[0], int(volunteer_id)))
            
            cherrypy.response.status = 201


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id=None, sportsman_count=0, total_task_count=0):
        with create_connection(self.args) as db:
            cur = db.cursor()
            command = 'SELECT * FROM volunteer_load WHERE sportsman_count >= %s AND total_task_count >= %s'
            if volunteer_id is not None:
                command += 'AND volunteer_id = %s'
                cur.execute(command, (sportsman_count, total_task_count, volunteer_id))
            else:
                cur.execute(command, (sportsman_count, total_task_count))
            result = cur.fetchall()
            return [{"volunteer_id": v[0], "volunteer_name": v[1], "sportsman_count": v[2], "total_task_count": v[3], "next_task_id": v[4], "next_task_time": str(v[5])} for v in result]


def run():
    cherrypy_cors.install()
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 12345,
    })
    config = {
        '/': {
            'cors.expose.on': True,
        },
    }
    cherrypy.quickstart(App(parse_cmd_line()), config=config)


if __name__ == '__main__':
    run()
