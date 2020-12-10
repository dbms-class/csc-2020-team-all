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

    # возвращает JSON с альбомами
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def albums(self, band_id = None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query_prefix = '''
              SELECT A.id AS id, A.name AS name, group_id AS band_id, COUNT(T.id) AS track_count
              FROM Album A 
              LEFT JOIN Track T ON A.id = T.album_id
              '''
            query_postfix = 'GROUP BY A.id'
            if band_id is None:
              cur.execute(query_prefix + query_postfix)
            else:
              cur.execute(f'''{query_prefix} WHERE A.group_id = {band_id} {query_postfix}''')
            return cur.fetchall()

    
    # обновляет содержание альбома 
    @cherrypy.expose
    def update_album(self, album_id, track_name, track_length = None):
      try:
        with create_connection(self.args) as db:
          cur = db.cursor()
          if track_length is None:
            cur.execute(f"INSERT INTO Track(name, album_id) VALUES ('{track_name}', {album_id})")
          else:
            cur.execute(f"INSERT INTO Track(name, album_id, duration_s) VALUES ('{track_name}', {album_id}, {track_length})")
        return 'Successfully'
      except BaseException as e:
        return str(e)
      


    # возвращает json с группами
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def bands(self):
      with create_connection(self.args) as db:
        cur = db.cursor()
        cur.execute('''
        SELECT G.id AS id, G.name AS name, CONCAT(R.name, ', ', C.name)
        FROM Groups G
        INNER JOIN Region R ON R.id = G.region_id
        INNER JOIN Country C ON C.id = R.country_id
        ''')
        return cur.fetchall()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_distributions(self, region_id=None, genre=None, carrier=None, year=None):
      if region_id is not None:
        try:
          region_id = int(region_id)
        except ValueError:
          return {"error": "invalid region_id"}

      if year is not None:
        try:
          year = int(year)
        except ValueError:
          return {"error": "invalid year"}

      def to_json(data):
        return {
          "region_id": data[0],
          "region_name": data[1],
          "carrier": data[2],
          "album_count": data[3]
        }

      with create_connection(self.args) as db:
        cur = db.cursor()

        params = {"region_id": region_id, "genre": genre, "carrier": carrier, "year": year}
        filters = {key: val for (key, val) in params.items() if val is not None}
        where = " and ".join([key + (" = %s" if key != "year" else " <= %s") for key in filters.keys()])

        query = """
          select
            a2.region_id,
            r.name as region_name,
            c.name as carrier,
            count(a.id) as album_count
          from album a
          join albuminregion a2 on a.id = a2.album_id
          join region r on a2.region_id = r.id
          join albumcarrierinregion a3 on a2.id = a3.album_info_id
          join carriertypes c on a3.carrier_id = c.id
          {}
          group by a2.region_id, r.name, c.name;
        """.format("where " + where if len(filters) > 0 else "")

        if len(filters) > 0:
          cur.execute(query, tuple(filters.values()))
        else:
          cur.execute(query)

        return list(map(to_json, cur.fetchall()))

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
