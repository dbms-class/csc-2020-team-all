# encoding: UTF-8

import json

import cherrypy
import cherrypy_cors

from connect import parse_cmd_line
from connect import connection_factory

from models import musician_tracks

@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def index(self):
        return "Hello web app"

    @cherrypy.expose
    @cherrypy.config()
    def bands(self):
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute("select id, name, location from bands_view")
            result = []
            bands_info = cur.fetchall()
            for b in bands_info:
                result.append({"id": b[0], "name": b[1], "location": b[2]})
            return json.dumps(result, ensure_ascii=False).encode('utf8')
        finally:
            connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def albums(self, band_id=None):
        if band_id is not None:
            try:
                band_id = int(band_id)
            except ValueError:
                return {'error': 'invalid band_id format'}

        def to_json(album):
            return {
                'id': album[0],
                'name': album[1],
                'band_id': album[2],
                'track_count': album[3]
            }

        
        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            query = '''
            select Album.id, work_name, group_id, count(Track.id)
            from Album left join Track
                on Album.id = Track.album_id
            {0}
            group by Album.id, work_name, group_id'''
            if band_id is not None:
                query = query.format('where group_id = %s')
                cur.execute(query, (band_id, ))
            else:
                query = query.format('')
                cur.execute(query)

            return list(map(to_json, cur.fetchall()))
        finally:
            connection_factory.putconn(db)
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update_album(album_id, track_name, track_length=None):
        try:
            album_id = int(album_id)
        except ValueError:
            return {'error': 'invalid album_id format'}

        if track_length is not None:
            try:
                track_length = int(track_length)
            except ValueError:
                return {'error': 'invalid track_length format'}

        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute('select * from Track where album_id = %s and track_name = %s', (album_id, track_name))
            if len(cur.fetchall()) > 0:
                return {'status': 'already exists'}
            
            cur.execute('insert into Track (album_id, name, length_in_seconds) values (%s, %s, %s) returning id', (album_id, track_name, track_length))

            return {'status': f'ok, id={cur.fetchall()}'}
        finally:
            connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_distributions(self, region_id=None, genre=None, carrier=None, year=None):
        if region_id is not None:
            try:
                region_id = int(region_id)
            except ValueError:
                return {'error': 'invalid region_id format'}
        if year is not None:
            try:
                year = int(year)
            except ValueError:
                return {'error': 'invalid year format'}

        def to_json(data):
            return {
                'region_id': data[0],
                'region_name': data[1],
                'carrier': data[2],
                'album_count': data[3]
            }

        db = connection_factory.getconn()
        try:
            cur = db.cursor()
            query = '''
            select region_id, Region.name, device, count(Album.id)
            from Album_production 
                left join Album on Album_production.album_id = Album.id
                left join Region on Album_production.region_id = Region.id
            {0}
            group by region_id, Region.name, device'''
            
            if any(it is not None for it in [region_id, genre, carrier, year]):
                where_clauses = []
                params = []
                if region_id is not None:
                    where_clauses.append('region_id = %s')
                    params.append(region_id)
                if genre is not None:
                    where_clauses.append('genre_name = %s')
                    params.append(genre)
                if carrier is not None:
                    where_clauses.append('device = %s')
                    params.append(carrier)
                if year is not None:
                    where_clauses.append('year_of_album_creation <= %s')
                    params.append(year)

                where_clause =  'where ' + ' and '.join(where_clauses)
                query = query.format(where_clause)
                print(query)
                cur.execute(query, tuple(params))
            else:
                query = query.format('')
                cur.execute(query)

            return list(map(to_json, cur.fetchall()))
        finally:
            connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def musician_unassign(self, musician_id, track_ids, blocked_tracks_album_id):
        all_tracks = list(map(
            lambda musician_track: musician_track.track,
            musician_tracks(musician_id)
        ))
        if track_ids != '*':
            track_ids_set = set(map(int, track_ids.split(',')))
            all_tracks = list(filter(
                lambda track: track.id in track_ids_set,
                all_tracks
            ))
        return list(map(lambda track: track.id, all_tracks))


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))