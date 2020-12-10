# encoding: UTF-8

## Веб сервер
import cherrypy
import json

from connect import parse_cmd_line
from connect import create_connection, connection_factory
from static import index

from model2 import db as sql_db, Stop, Route, RouteStop, Timetable
from peewee import *
from playhouse.shortcuts import model_to_dict


def default(obj):
       """Default JSON serializer."""
       import calendar, datetime

       if isinstance(obj, datetime.datetime):
           if obj.utcoffset() is not None:
               obj = obj - obj.utcoffset()
           millis = int(
               calendar.timegm(obj.timetuple()) * 1000 +
               obj.microsecond / 1000
           )
           return millis
       raise TypeError('Not sure how to serialize %s' % (obj,))

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
      if (not _time.isnumeric() and not(1 <= int(_time) and int(_time) <= 1440)):
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
    def get_timetable(self, stop_id=None, route_id=None, is_working_day=True, with_extremes=False):
        if stop_id is None:
            return
        # db = connection_factory.getconn()
        sql_db.connect()
        try:
            q = Timetable.select();
            is_working_day = bool(int(is_working_day))
            q = q.where(Timetable.is_working_day != (not is_working_day))
            q = q.where(Timetable.stop_id == stop_id)
            if route_id is not None:
                q = q.where(Timetable.route_id == route_id)
            ans = [item for item in q]
            if with_extremes:
                ans = [{'stop_id': item.stop_id, 'stop_name': item.stop_name, 'route_num': item.route_num, 'route_first_arrival': str(item.route_first_arrival), 'route_last_arrival': str(item.route_last_arrival), 'all_first_arrival': str(item.all_first_arrival), 'all_last_arrival': str(item.all_last_arrival)} for item in q]
            else:
                ans = [{'stop_id': item.stop_id, 'stop_name': item.stop_name, 'route_num': item.route_num, 'route_first_arrival': str(item.route_first_arrival), 'route_last_arrival': str(item.route_last_arrival)} for item in q]
            return ans
        finally:
            # connection_factory.putconn(db)
            sql_db.close()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def shift_timetable(self, route_num, stop_ids, start_min=0, end_min=1440, shift_min, is_working_day):

      if (not route_num.isnumeric()):
          return {"error": "route_num is not numeric"}
      if (not start_min.isnumeric())
          return {"error": "start_min is not numeric"}
      start_min = int(start_min)
      if (not end_min.isnumeric())
          return {"error": "end_min is not numeric"}
      end_min = int(end_min)
      if (not is_working_day.isnumeric())
          return {"error": "is_working_day is not numeric"}
      if (not shift_min.isnumeric()):
          return {"error": "shift_min is not numeric"}
      shift_min = int(shift_min)
      is_working_day = int(is_working_day)
      if is_working_day == 0:
          is_working_day = False
      elif is_working_day == 1:
          is_working_day = True
      else:
          return {"error": "is_working_day is neither 0 nor 1"}
          

      all_stops = (list_str_stops == '*')
      if !all_stops:
          stops_to_change = []
          list_str_stops = stop_ids.split(',')
          for str_stop in list_str_stops:
              stop_platform = str_stop.split('-')
              if len(stop_platform) != 2:
                  return
              if not stop_platform[0].isnumeric() or not stop_platform[1].isnumeric():
                  return
              stop = int(stop_platform[0])
              platform = int(stop_platform[1])
              stops_to_change.append((stop, platform))

      query = ''
          





cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))
