# encoding: UTF-8

## Веб сервер
import cherrypy
import my_model
import cherrypy_cors
import re

from connect import parse_cmd_line, connection_factory
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
        return list(map(
            lambda p: {
                "id": p.id,
                "name": p.get_name()
            },
            my_model.all_countries()
        ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteers(self):
        return list(map(
            lambda p: {
                "id": p.id,
                "name": p.get_name(),
                "phone": p.get_phone()
            },
            my_model.all_volunteers()
        ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def athlets(self):
        return list(map(
            lambda p: {
                "id": p.id,
                "name": p.get_name(),
                "delegation_id": p.get_delegation_id(),
                "volunteer_id": p.get_volunteer_id()
            },
            my_model.all_athlets()
        ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def register(self, sportsman, country, volunteer_id):
        # http://csc-2020-team-all-1.dmitrybarashev.repl.co/register?country=Country1&sportsman=asd&volunteer_id=1
        delegation = my_model.get_delegation(country)
        try:
            if delegation is None:
                raise cherrypy.HTTPError(404, "There is no delegation for country " + country)

            if my_model.all_volunteers(volunteer_id) is None:
                raise cherrypy.HTTPError(404, "There is no volunteer id=" + volunteer_id)
        except cherrypy.HTTPError:
            cherrypy.response.status = 400

        if my_model.register_athlete(sportsman, country, volunteer_id):
            cherrypy.response.status = 201
        else:
            cherrypy.response.status = 400

    connection_factory
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def volunteer_load(self, volunteer_id=None, sportsman_count=0, total_task_count=0):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            command = 'SELECT * FROM volunteer_load WHERE sportsman_count >= %s AND total_task_count >= %s'
            if volunteer_id is not None:
                command += ' AND volunteer_id = %s'
                cur.execute(command, (sportsman_count, total_task_count, volunteer_id))
            else:
                cur.execute(command, (sportsman_count, total_task_count))
            result = cur.fetchall()
            return [{"volunteer_id": v[0], "volunteer_name": v[1], "sportsman_count": v[2], "total_task_count": v[3],
                     "next_task_id": v[4], "next_task_time": str(v[5])} for v in result]
        finally:
            connection_factory.putconn(db)


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
