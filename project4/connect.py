# encoding: UTF-8

import argparse
import psycopg2 as pg_driver

def parse_cmd_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pg-host', help='PostgreSQL host name', default='rogue.db.elephantsql.com')
    parser.add_argument('--pg-port', help='PostgreSQL port', default=5432)
    parser.add_argument('--pg-user', help='PostgreSQL user', default='wzkpgldt')
    parser.add_argument('--pg-password', help='PostgreSQL password', default='94bLQvMSgEWS3RhZD9kQuL9lqSplKlzM')
    parser.add_argument('--pg-database', help='PostgreSQL database', default='wzkpgldt')
    return parser.parse_args()

# Создаёт подключение к постгресу в соответствии с аргументами командной строки.
def create_connection_pg(args):
    return pg_driver.connect(user=args.pg_user, password=args.pg_password, host=args.pg_host, port=args.pg_port)


# Создаёт подключение в соответствии с аргументами командной строки.
def create_connection(args):
    return create_connection_pg(args)