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
    def users(self, user_id=None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            if user_id is None:
                cur.execute("SELECT id, name FROM Users")
            else:
                cur.execute("SELECT id, name FROM Users WHERE id=%s", user_id)
            result = []
            users = cur.fetchall()
            for u in users:
                result.append({"id": u[0], "name": u[1]})
            return result


def main():
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
    main()
