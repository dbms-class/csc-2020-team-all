#!bin/sh
#pip install cherrypy psycopg2-binary
#pip install peewee

PG_HOST=hattie.db.elephantsql.com
PG_PORT=5432
PG_USER=kzlmjwbt
PG_DATABASE=kzlmjwbt
PG_PASSWORD=iw0hP194HMtssZgOHyhie-10mmPTDB6a

cd project7

# добавляем таблички и загружаем тестовые данные
python create_db.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE

python webapp.py --pg-host $PG_HOST --pg-port $PG_PORT --pg-user $PG_USER --pg-password $PG_PASSWORD --pg-database $PG_DATABASE