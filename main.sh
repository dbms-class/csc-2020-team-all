##!bin/sh
#pip install cherrypy psycopg2-binary

PG_HOST=hattie.db.elephantsql.com
PG_PORT=5432
PG_USER=ujrazvgd
PG_DATABASE=ujrazvgd
PG_PASSWORD=WVHDSjU8ZURw6S-S7gc4Z5Ij1EoNQP8t

# Upload schemes and test data to db. Usage example:
#cd project12 && python3 upload_db.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE

# App. Usage example:
cd project12 && python3 webapp.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE