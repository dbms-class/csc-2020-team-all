# pip install cherrypy cherrypy_cors psycopg2-binary peewee

PG_HOST=hattie.db.elephantsql.com
PG_PORT=5432
PG_USER=ujrazvgd
PG_DATABASE=ujrazvgd
PG_PASSWORD=<password>

cd project8

# Upload schemes and test data to db by psql. Usage example (needs interactive password input):
# psql -h $PG_HOST -p $PG_PORT -U $PG_USER -f project8.sql
# psql -h $PG_HOST -p $PG_PORT -U $PG_USER -f testdata.sql

# Another way:
# psql postgres://ujrazvgd:<password>@hattie.db.elephantsql.com:5432/ujrazvgd -f project8.dsql

# Upload schemes and test data to db. Usage example:
python upload_db.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE

# App. Usage example:
python webapp.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE
