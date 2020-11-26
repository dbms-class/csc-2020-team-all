# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import connection_factory
from connect import parse_cmd_line

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
    def stops(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute("SELECT id, address, available_platforms FROM stop S;")
            stops = cur.fetchall()
            result = [
                {"id": s[0], "address": s[1], "platforms": s[2]}
                for s in stops
            ]
        finally:
            connection_factory.putconn(db)
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def routes(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute("SELECT id, initial_stop, final_stop FROM route R;")
            routes = cur.fetchall()
            result = [
                {"route": r[0], "start_stop_id": r[1], "end_stop_id": r[2]}
                for r in routes
            ]
        finally:
            connection_factory.putconn(db)
        return result

    @cherrypy.expose
    def update_timetable(self, stop_id, platform, time, route_id, is_working_day):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            print("POST PARAMS: {0}, {1}, {2}, {3}, {4}".format(stop_id, platform, time, route_id, is_working_day))

            cur.execute(
                "INSERT INTO timetable(stop_id, time_min, route_id, platform_number, is_weekend) VALUES(%s, %s, %s, %s, %s);",
                (stop_id, time, route_id, platform,
                 bool(is_working_day)))
        finally:
            db.commit()
            connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_timetable(self, stop_id, route_id=None, is_working_day=True, with_extremes=None):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()

            if (route_id):
                cur.execute("SELECT * FROM TimetableStopView WHERE stop_id=%s AND route_id=%s AND is_weekend=%s",
                            (stop_id, route_id, bool(is_working_day)))
            else:
                cur.execute("SELECT * FROM TimetableStopView WHERE stop_id=%s AND is_weekend=%s",
                            (stop_id, bool(is_working_day)))

            grouped_data = cur.fetchall()
            result = [
                {"stop_id": g[0], "stop_name": g[1], "route_num": g[2], "route_first_arrival": g[3],
                 "route_last_arrival": g[4]
                 }
                for g in grouped_data
            ]

            if (with_extremes):
                cur.execute("SELECT * FROM TimetableStopSimpleView WHERE stop_id=%s", stop_id)
                for g in cur.fetchall():
                    for r in result:
                        r.update(all_first_arrival=g[1], all_last_arrival=g[2])
        finally:
            connection_factory.putconn(db)
        return result


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
