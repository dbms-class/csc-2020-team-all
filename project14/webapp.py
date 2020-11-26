import cherrypy

from connect import parse_cmd_line
from connect import create_connection
from static import index

@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def index(self):
      return index()
    
    # не генерится идентификатор для таблицы Track при вставке
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update_album(self, album_id, track_name, track_length=None):
      with create_connection(self.args) as db:
        cur = db.cursor()
        cur.execute("SELECT id FROM Track WHERE album_id=? AND name=?", (album_id, track_name))

        track_id = cur.fetchone()
        if not track_id is None:
          if track_length is None:
            raise cherrypy.HTTPError(status=400)
          
          cur.execute("UPDATE Track SET length_s=? WHERE id=?", (track_length, track_length))
        else:
          cur.execute("INSERT INTO Track (name, album_id, length_s) VALUES (?, ?, ?)", (track_name, album_id, track_length))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def bands(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name, country, city FROM Band")
            bands = cur.fetchall()

            result = []
            for band in bands:
                result.append({
                    "id": band[0],
                    "name": band[1],
                    "location": f"{band[3]}, {band[2]}"
                })
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def albums(self, band_id=None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            if band_id is None:
                cur.execute("""
                    WITH album_track_counts AS (
                        SELECT album_id, COUNT(id) as track_count
                        FROM Track
                        GROUP BY album_id
                    )
                    SELECT A.id, A.name, A.band_id, album_track_counts.track_count
                    FROM Album A LEFT JOIN album_track_counts ON a.id=album_track_counts.album_id""")
            else:
                raise NotImplementedError
            albums = cur.fetchall()

            result = []
            for album in albums:
                result.append(dict(zip(["id", "name", "band_id", "track_count"], album)))
            return result


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))


# INSERT INTO Band(id, name, country, city) VALUES (1, "a", "b", "c");
# INSERT INTO Album(id, name, band_id) VALUES (1, "a", 1);
# INSERT INTO Track(id, name, length_s) VALUES (1, "1", 34), (2, "2", 45), (3, "3", 12);