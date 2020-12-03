# encoding: UTF-8

import argparse

# Драйвер PostgreSQL
# Находится в модуле psycopg2-binary, который можно установить командой
# pip install psycopg2-binary или её аналогом.
import psycopg2 as pg_driver
# Драйвер SQLite3
# Находится в модуле sqlite3, который можно установить командой
# pip install sqlite3 или её аналогом.
import sqlite3 as sqlite_driver


# Разбирает аргументы командной строки.
# Выплевывает структуру с полями, соответствующими каждому аргументу.
def parse_cmd_line():
    parser = argparse.ArgumentParser(description='Эта программа вычисляет 2+2 при помощи реляционной СУБД')
    parser.add_argument('--pg-host', help='PostgreSQL host name', default='localhost')
    parser.add_argument('--pg-port', help='PostgreSQL port', default=5432)
    parser.add_argument('--pg-user', help='PostgreSQL user', default='')
    parser.add_argument('--pg-password', help='PostgreSQL password', default='')
    parser.add_argument('--pg-database', help='PostgreSQL database', default='')
    parser.add_argument('--sqlite-file', help='SQLite3 database file. Type :memory: to use in-memory SQLite3 database',
                        default='sqlite.db')
    return parser.parse_args()


# Создаёт подключение к постгресу в соответствии с аргументами командной строки.
def create_connection_pg(args):
    return pg_driver.connect(user=args.pg_user, password=args.pg_password, host=args.pg_host, port=args.pg_port)


# Создаёт подключение к SQLite в соответствии с аргументами командной строки.
def create_connection_sqlite(args):
    return sqlite_driver.connect(args.sqlite_file)


# Создаёт подключение в соответствии с аргументами командной строки.
# Если указан аргумент --sqlite-file то создается подключение к SQLite,
# в противном случае создаётся подключение к PostgreSQL
def create_connection(args):
    if args.sqlite_file is not None:
        return create_connection_sqlite(args)
    else:
        return create_connection_pg(args)


class ConnectionFactory:
    def __init__(self, open_fxn, close_fxn, create_db_fxn):
        self.create_db_fxn = create_db_fxn
        self.open_fxn = open_fxn
        self.close_fxn = close_fxn


    def getconn(self):
        return self.open_fxn()

    def putconn(self, conn):
        return self.close_fxn(conn)

    def create_db(self):
        return self.create_db_fxn()


def create_connection_factory(args):
    # Создаёт подключение к SQLite в соответствии с аргументами командной строки.
    def open_sqlite():
        return sqlite_driver.connect(args.sqlite_file)

    def close_sqlite(conn):
        pass

    def create_db_sqlite():
        return PooledSqliteDatabase(args.sqlite_file)

    # Создаёт подключение в соответствии с аргументами командной строки.
    # Если указан аргумент --sqlite-file то создается подключение к SQLite,
    # в противном случае создаётся подключение к PostgreSQL
    if args.sqlite_file is not None:
        return ConnectionFactory(open_fxn=open_sqlite, close_fxn=close_sqlite, create_db_fxn=create_db_sqlite)
    else:

        def open_pg():
            return connect(f"postgres+pool://{args.pg_user}:{args.pg_password}@{args.pg_host}:{args.pg_port}/{args.pg_database}")

        def close_pg(conn):
            conn.close()

        def create_db_pg():
            return LoggingDatabase(args)

        return ConnectionFactory(open_fxn=open_pg, close_fxn=close_pg, create_db_fxn=create_db_pg)


connection_factory = create_connection_factory(parse_cmd_line())