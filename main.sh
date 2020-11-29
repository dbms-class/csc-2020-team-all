#!bin/sh
#pip install cherrypy psycopg2-binary

PG_HOST=hattie.db.elephantsql.com
PG_PORT=5432
PG_USER=ujrazvgd
PG_DATABASE=ujrazvgd
PG_PASSWORD=<password>

# Upload schemes and test data to db. Usage example:
# cd project12 && python upload_db.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE

# App. Usage example:
cd project12 && python webapp.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE
