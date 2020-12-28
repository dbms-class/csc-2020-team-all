from connect import connection_factory
from peewee import *

db = connection_factory.create_db()

class CountryEntity(Model):
    id = AutoField()
    name = CharField()

    class Meta:
        database = db
        table_name = 'countries'


def all_countries():
    q = CountryEntity.select()
    return [Country(p) for p in q]


class Country:
    def __init__(self, entity):
        self.entity = entity
        self.id = entity.id

    def get_name(self):
        return self.entity.name


class VolunteerEntity(Model):
    id = AutoField()
    name = CharField()
    phone = CharField()

    class Meta:
        database = db
        table_name = 'volunteers'


def all_volunteers(volunteer_id=None):
    q = VolunteerEntity.select()
    if volunteer_id is not None:
        q = q.where(VolunteerEntity.id == volunteer_id)
    return [Volunteer(p) for p in q]


def all_athlets():
    q = AthletEntity.select()
    return [Athlet(p) for p in q]


class Volunteer:
    def __init__(self, entity):
        self.entity = entity
        self.id = entity.id

    def get_name(self):
        return self.entity.name

    def get_phone(self):
        return self.entity.phone


class DelegationEntity(Model):
    id = AutoField()
    country_id = ForeignKeyField(CountryEntity, backref="Country", column_name="id")

    class Meta:
        database = db
        table_name = 'countries_delegation'


def get_delegation(country_name):
    q = DelegationEntity.select()
    country_id = get_country_id_from_name(country_name)
    if country_id is None:
        return None
    q = q.where(DelegationEntity.country_id == country_id)
    return Delegation(q[0])


def get_country_id_from_name(country_name):
    try:
        country = CountryEntity.select().where(CountryEntity.name == country_name).get()
        return country.id
    except:
        return None


class Delegation:
    def __init__(self, entity):
        self.entity = entity
        self.id = entity.id
        self.country_id = entity.country_id

    def get_name(self):
        return self.entity.name

    def get_country_id(self):
        return self.country_id


class AthletEntity(Model):
    id = AutoField()
    name = CharField()
    delegation_id = ForeignKeyField(DelegationEntity, backref='countries_delegation', column_name='delegation_id')
    volunteer_id = ForeignKeyField(VolunteerEntity, backref='volunteers', column_name='volunteer_id')

    class Meta:
        database = db
        table_name = 'athletes'


class Athlet:
    def __init__(self, entity):
        self.entity = entity
        self.id = entity.id
        self.name = entity.name
        self.delegation_id = entity.delegation_id
        self.volunteer_id = entity.volunteer_id

    def get_name(self):
        return self.entity.name

    def get_delegation_id(self):
        return self.entity.delegation_id.id

    def get_volunteer_id(self):
        return self.entity.volunteer_id.id


def register_athlete(name, country_name, volunteer_id):
    delegation_id = get_delegation(country_name).id
    if delegation_id is None:
        return False
    if name.isdigit():
        athlet = AthletEntity.get(id=name)
        if athlet:
            athlet.delegation_id = delegation_id
            athlet.volunteer_id = volunteer_id
            athlet.save()
            return True
        return False
    else:
        AthletEntity.create(name=name, delegation_id=delegation_id, volunteer_id=volunteer_id)
        return True

    # nextId = athletes.select(fn.MAX(athletes.c.id)).scalar() + 1

    # athletes.insert(name=name, delegation_id=delegation_id, volunteer_id=volunteer_id).execute()
    # return athletes.update(distance=distance).where(athletes.c.id == nextId).execute() == 1
