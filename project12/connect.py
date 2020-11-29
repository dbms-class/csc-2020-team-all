import argparse

# Драйвер PostgreSQL
import psycopg2 as pg_driver
# Драйвер SQLite3
import sqlite3 as sqlite_driver


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


def create_connection_pg(args):
    return pg_driver.connect(user=args.pg_user, password=args.pg_password, host=args.pg_host, port=args.pg_port,
                             dbname=args.pg_database)


def create_connection_sqlite(args):
    return sqlite_driver.connect(args.sqlite_file)


def create_connection(args):
    if args.sqlite_file is not None:
        print('Use SQLite')
        return create_connection_sqlite(args)
    else:
        print('Use Postgres')
        return create_connection_pg(args)