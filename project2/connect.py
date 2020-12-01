# encoding: UTF-8
import pdb
import argparse

# Драйвер PostgreSQL
# Находится в модуле psycopg2-binary, который можно установить командой
# pip install psycopg2-binary или её аналогом.
import psycopg2 as pg_driver
from psycopg2 import pool

# Драйвер SQLite3
# Находится в модуле sqlite3, который можно установить командой
# pip install sqlite3 или её аналогом.
import sqlite3 as sqlite_driver

from contextlib import contextmanager
from playhouse.db_url import connect
# Разбирает аргументы командной строки.
# Выплевывает структуру с полями, соответствующими каждому аргументу.
def parse_cmd_line():
    parser = argparse.ArgumentParser(description='Эта программа вычисляет 2+2 при помощи реляционной СУБД')
    parser.add_argument('--pg-host', help='PostgreSQL host name', default='rogue.db.elephantsql.com')
    parser.add_argument('--pg-port', help='PostgreSQL port', default=5432)
    parser.add_argument('--pg-user', help='PostgreSQL user', default='mvyaqpsr')
    parser.add_argument('--pg-password', help='PostgreSQL password', default='xxNdOvw2zYTlVulbXCwXVeAoJD8VY1kA')
    parser.add_argument('--pg-database', help='PostgreSQL database', default='mvyaqpsr')
    parser.add_argument('--sqlite-file', help='SQLite3 database file. Type :memory: to use in-memory SQLite3 database', default=None)
    return parser.parse_args()

# #открываем и закрываем сессии
# def create_connection(args):
#     #print(args)
#     if args.sqlite_file is not None:
#         print('Use SQLite')
#         return sqlite_driver.connect(args.sqlite_file)
#     else:
#         #print('Use Postgres')
#         return pg_driver.connect(user=args.pg_user, password=args.pg_password, host=args.pg_host, port=args.pg_port, dbname=args.pg_database)

#класс отвечающий за создания пулла сессий
#берем свободную и возвращаем назад
class ConnectionFactory:
    def __init__(self, open_fxn, close_fxn):
        self.open_fxn = open_fxn
        self.close_fxn = close_fxn

    def getconn(self):
        return self.open_fxn()

    def putconn(self, conn):
        return self.close_fxn(conn)

    @contextmanager
    def conn(self):
        try:
            result = self.open_fxn()
            yield result
        finally:
            self.close_fxn(result)

def create_connection_factory(args):
    # Создаёт подключение в соответствии с аргументами командной строки.
    # Если указан аргумент --sqlite-file то создается подключение к SQLite,
    # в противном случае создаётся подключение к PostgreSQL
    if args.sqlite_file is not None:
        #print('SQLITE')
        def open_sqlite():
            return sqlite_driver.connect(args.sqlite_file)

        def close_sqlite(conn):
            pass

        return ConnectionFactory(open_fxn=open_sqlite, close_fxn=close_sqlite)
    else:
        #print('POSTGRE')
        def open_pg():
            return connect(f"postgres+pool://{args.pg_user}:{args.pg_password}@{args.pg_host}:{args.pg_port}/{args.pg_database}")

        def close_pg(conn):
            conn.close()

        return ConnectionFactory(open_fxn=open_pg, close_fxn=close_pg)