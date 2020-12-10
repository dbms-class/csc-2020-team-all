#!bin/sh
#pip install cherrypy psycopg2-binary
#pip install peewee

PG_HOST=rogue.db.elephantsql.com
PG_PORT=5432
PG_USER=cyhezogi
PG_DATABASE=cyhezogi
PG_PASSWORD=Q_CGeI1nCFM_kYLH7O8ZmKe9XSq-dE3D

cd project7

# добавляем таблички и загружаем тестовые данные
#python create_db.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE

python webapp.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE