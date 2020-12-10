from connect import connection_factory
from peewee import *

db = connection_factory.create_db()

class Substance(Model):
  name = CharField(primary_key=True)
  formula = CharField()

  class Meta:
    database = db
    table_name = 'substance'


class Lab(Model):
  id = AutoField()
  name = CharField(unique=True)
  head_last_name = CharField()

  class Meta:
    database = db
    table_name = 'lab'


class Certificate(Model):
  id = AutoField()
  expiration_date = DateField(),
  lab = ForeignKeyField(Lab,  backref="certificate", column_name="lab_id")
  
  class Meta:
    database = db
    table_name = 'certificate'


class DrugForm(Model):
  id = AutoField()
  name = CharField(unique=True)

  class Meta:
    database = db
    table_name = 'drug_form'

class ReleasePackage(Model):
  id = AutoField()
  name = CharField(unique=True)

  class Meta:
    database = db
    table_name = 'release_package'


class Drug(Model):
  id = AutoField()
  trademark = CharField()
  international_name = CharField()
  drug_form = ForeignKeyField(DrugForm, backref="drug", column_name="drug_form_id")
  substance_name = ForeignKeyField(Substance, backref="drug", column_name="substance_name")
  certificate = ForeignKeyField(Certificate, backref="drug", column_name="certificate_id")
  release_package_id = ForeignKeyField(ReleasePackage, backref="drug", column_name="release_package_id")

  class Meta:
    database = db
    table_name = 'drug'


class DrugStore(Model):
  id = AutoField()
  name = CharField()
  address = CharField()

  class Meta:
    database = db
    table_name = 'drugstore'


class DrugStorePriceList(Model):
  drugstore = ForeignKeyField(DrugStore, backref="price_list", column_name="drugstore_id")
  drug = ForeignKeyField(Drug, backref="price_list", column_name="drug_id")
  price = DecimalField(null=False, constraints=[Check('price > 0.0')])
  items_count = IntegerField(null=False, constraints=[Check('items_count >= 0')])

  class Meta:
    database = db
    primary_key = CompositeKey('drugstore', 'drug')
    table_name = 'drugstore_price_list'
