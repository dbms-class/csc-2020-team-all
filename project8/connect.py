#
import argparse

# Драйвер SQLite3
import sqlite3 as sqlite_driver

from contextlib import contextmanager
from playhouse.db_url import connect


# Разбирает аргументы командной строки.
def parse_cmd_line():
    parser = argparse.ArgumentParser(description='Эта программа учёта лекарств в аптеках')
    parser.add_argument('--pg-host', help='PostgreSQL host name', default='localhost')
    parser.add_argument('--pg-port', help='PostgreSQL port', default=5432)
    parser.add_argument('--pg-user', help='PostgreSQL user', default='')
    parser.add_argument('--pg-password', help='PostgreSQL password', default='')
    parser.add_argument('--pg-database', help='PostgreSQL database', default='')
    parser.add_argument('--sqlite-file', help='SQLite3 database file. Type :memory: to use in-memory SQLite3 database',
                        default=None)
    return parser.parse_args()


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
    # Создаёт подключение к SQLite в соответствии с аргументами командной строки.
    def open_sqlite():
        return sqlite_driver.connect(args.sqlite_file)

    def close_sqlite(conn):
        pass

    # Создаёт подключение в соответствии с аргументами командной строки.
    # Если указан аргумент --sqlite-file то создается подключение к SQLite,
    # в противном случае создаётся подключение к PostgreSQL
    if args.sqlite_file is not None:
        return ConnectionFactory(open_fxn=open_sqlite, close_fxn=close_sqlite)
    else:

        def open_pg():
            return connect(f"postgres+pool://{args.pg_user}:{args.pg_password}@{args.pg_host}:{args.pg_port}/{args.pg_database}")

        def close_pg(conn):
            conn.close()

        return ConnectionFactory(open_fxn=open_pg, close_fxn=close_pg)