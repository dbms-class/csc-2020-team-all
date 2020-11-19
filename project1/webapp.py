# encoding: UTF-8

## Веб сервер
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
    def register(self, sportsman, country, volunteer_id, height, weight, age, gender=None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT * FROM Countries_delegation WHERE country_name = %s", (str(country),))
            country_database = cur.fetchone()
            print(country_database)
            if country_database is None:
                raise cherrypy.HTTPError(
                    400,
                    f"There is no delegation for country {country}"
                )

            a = cur.execute(
                "INSERT INTO Athletes (name, gender, height, weight, age, delegation_id, volunteer_id) values (%s, "
                "%s, %s, %s, %s, %s, %s)",
                (sportsman, gender, int(height), int(weight), int(age), country_database[0], int(volunteer_id)))
            print(a)

            return {"id": country_database[0], "name": country_database[1]}


def run():
    cherrypy_cors.install()
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
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
