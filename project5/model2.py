from peewee import *


db = SqliteDatabase('sqlite.db')


class BaseModel(Model):
    class Meta:
        database = db


class TransportType(BaseModel):
  id = AutoField()
  name = TextField(unique=True, null=False)

  class Meta:
    table_name = 'transport_type'


class Stop(BaseModel):
  id = AutoField()
  address = TextField(unique = True, null=False)
  number_of_platforms = IntegerField(null=False)

  class Meta:
    table_name = 'transport_stop'


class Route(BaseModel):
  id = AutoField()
  route = IntegerField(unique = True, null=False)
  transport_type = ForeignKeyField(TransportType, backref="transport_route", null=False)
  first_stop = ForeignKeyField(Stop, backref="transport_route", null=False)
  last_stop = ForeignKeyField(Stop, backref="transport_route", null=False)

  class Meta:
    table_name = 'transport_route'


class RouteStop(BaseModel):
  route = ForeignKeyField(Route, backref="route_stop", null=False)
  stop = ForeignKeyField(Stop, backref="route_stop", null=False)
  platform_number = IntegerField(null = False)
  arrival_time = TimeField(null = False)
  is_working_day = BooleanField(null = False)

  class Meta:
    table_name = 'route_stop'
    primary_key = False