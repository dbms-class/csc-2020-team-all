# encoding: UTF-8

## Веб сервер
import cherrypy
import json

from connect import parse_cmd_line
from connect import create_connection, connection_factory
from static import index

from model2 import db as sql_db, Stop, Route, RouteStop
from peewee import *
from playhouse.shortcuts import model_to_dict


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
    def update_timetable(self, stop_id, platform, _time, route_id, is_working_day=1):
      if (not is_working_day.isnumeric() and (int(is_working_day) not in [0, 1])):
          return
      if (not stop_id.isnumeric()):
          return
      if (not platform.isnumeric()):
          return
      if (not _time.isnumeric() and not(1 <= int(_time) <= 1440)):
          return
      if (not route_id.isnumeric()):
          return

      db = create_connection(self.args)
      cur = db.cursor()
      cur.execute(f"SELECT * FROM route_stop WHERE route_id={route_id} \
                    and stop_id={stop_id} \
                    and platform_number={platform} \
                    and is_working_day={True if is_working_day else False};")
      result = cur.fetchall()

      if len(result) == 0: 
        cur.execute(f"INSERT INTO \
                      route_stop (route_id, stop_id, platform_number, arrival_time, is_working_day) \
                      VALUES({route_id}, \
                             {stop_id}, \
                             {platform}, \
                             interval '{_time} minute'::TIME, \
                             {True if is_working_day else False};"
                    )
      else:
        cur.execute(f"UPDATE route_stop \
                      SET arrival_time = interval '{_time} minute'::TIME \
                      WHERE route_id={route_id} \
                        and stop_id={stop_id} \
                        and platform_number={platform} \
                        and is_working_day={True if is_working_day else False};"
                    )

      cur.close()
      return

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def routes_alt(self):
      sql_db.connect()
      try:
        routes = [model_to_dict(item) for item in Route.select()]
        return json.dumps(routes)
      finally:
        sql_db.close()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def routes(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, route, first_stop_id, last_stop_id FROM transport_route")
            result = []
            routes = cur.fetchall()
            for r in routes:
              result.append({"id": r[0], "route": r[1],"start_stop_id": r[2], "end_stop_id": r[3]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stops_alt(self):
      sql_db.connect()
      try:
        stops = [model_to_dict(item) for item in Stop.select()]
        return json.dumps(stops)
      finally:
        sql_db.close()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def stops(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, address, number_of_platforms FROM transport_stop")
            result = []
            stops = cur.fetchall()
            for s in stops:
              result.append({"id": s[0], "address": s[1],"number_of_platforms": s[2]})
            return result

    # select что-хотим WHERE даненые
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_timetable(self, stop_id=None, route_id=None, is_working_day=True, with_extremes=None):
        # if stop_id is None:
            # return
        #db = connection_factory.getconn()
        sql_db.connect()
        try:
            q = RouteStop.select()
            return json.dumps([model_to_dict(item) for item in q], default=json_util.default)
            # routeStopView = Table('transport_condition').bind(db)
            # stopView = Table('transport_stop').bind(db)
            # q = routeStopView.select()
            # q = routeStopView.select(routeStopView.c.route_id)#, routeStopView.c.stop_id, routeStopView.c.platform_number, routeStopView.c.arrival_time, routeStopView.c.is_working_day)
            # q = q.join(stopView).where(stopView.c.id == routeStopView.c.stop_id)
            #if stop_id is not None:
            #  q = q.where(routeStopView.c.stop_id == stop_id)
            #if route_id is not None:
            #    q = q.where(routeStopView.c.route_id == route_id)
            #q = q.where(routeStopView.c.is_working_day == is_working_day)
            #q = q.order_by(routeStopView.c.arrival_time.asc())
            # ans = [p for p in q]
            # if with_extremes:
            #     if route_id is not None:
            #         qq = routeStopView.select(routeStopView.c.route_id, routeStopView.c.stop_id, routeStopView.c.platform_number, routeStopView.c.arrival_time, routeStopView.c.is_working_day)
            #         qq = qq.where(routeStopView.c.stop_id == stop_id)
            #         qq = qq.where(routeStopView.c.is_working_day == is_working_day)
            #         qq = qq.order_by(routeStopView.c.arrival_time.asc())
            #         qq = qq.objects(routeStopView)
            #         all_ans = [p for p in qq]
            #     else:
            #         all_ans = copy(ans)
            # return ans
        finally:
            # connection_factory.putconn(db)
            sql_db.close()

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
