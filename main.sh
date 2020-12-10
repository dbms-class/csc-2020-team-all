#!/bin/bash
#pip install cherrypy psycopg2-binary

export PG_HOST=kandula.db.elephantsql.com
export PG_PORT=5432
export PG_USER=iviswxah
export PG_DATABASE=iviswxah
export PG_PASSWORD=5W2zAuI6Yv_MtbFd05Ab_3I4_3RUEWU2

# Upload schemes and test data to db. Usage example:
#cd project12 && python upload_db.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE

# App. Usage example:
cd project12 && python webapp.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE
