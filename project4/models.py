from connect import connection_factory
from peewee import *


db = connection_factory.create_db()

def txn(work):
    with db.atomic() as txn:
        return work(db)


class AlbumEntity(Model):
    id = AutoField()

    class Meta:
        database = db
        table_name = 'album'

class TrackEntity(Model):
    id = AutoField()
    album = ForeignKeyField(AlbumEntity, backref='tracks', column_name='album_id')
    
    class Meta:
        database = db
        table_name = 'track'

class MusicianEntity(Model):
    id = AutoField()

    class Meta:
        database = db
        table_name = 'musician'

class MusicianTrackEntity(Model):
    musician = ForeignKeyField(MusicianEntity, backref='track', column_name='musician_id')
    track = ForeignKeyField(TrackEntity, backref='musician', column_name='track_id')
    role_id = IntegerField()

    class Meta:
        database = db
        table_name = 'musician_track'

def musician_tracks(musician_id):
    return MusicianTrackEntity.select(
        MusicianTrackEntity.musician,
        MusicianTrackEntity.track,
        MusicianTrackEntity.role_id
    ).join(
        MusicianEntity
    ).where(
        MusicianEntity.id == musician_id
    )
