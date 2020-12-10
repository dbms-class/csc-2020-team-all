# encoding: UTF-8

import argparse
import logging

from playhouse.pool import PooledPostgresqlDatabase, PooledSqliteDatabase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Драйвер PostgreSQL
# Находится в модуле psycopg2-binary, который можно установить командой
# pip install psycopg2-binary или её аналогом.
import psycopg2 as pg_driver
from psycopg2 import pool
from psycopg2.extras import LoggingConnection

# Драйвер SQLite3
# Находится в модуле sqlite3, который можно установить командой
# pip install sqlite3 или её аналогом.
import sqlite3 as sqlite_driver

from contextlib import contextmanager
from playhouse.db_url import connect


def parse_cmd_line():
  parser = argparse.ArgumentParser()
  parser.add_argument('--pg-host', help='PostgreSQL host name', default='rogue.db.elephantsql.com')
  parser.add_argument('--pg-port', help='PostgreSQL port', default=5432)
  parser.add_argument('--pg-user', help='PostgreSQL user', default='lfiykhno')
  parser.add_argument('--pg-password', help='PostgreSQL password', default='NVm2RUHJXAq8CMQ8ZGrAbzTww1orBUIP')
  parser.add_argument('--pg-database', help='PostgreSQL database', default='lfiykhno')
  parser.add_argument('--sqlite-file', help='SQLite3 database file. Type :memory: to use in-memory SQLite3 database', default=None)
  return parser.parse_args()

class LoggingDatabase(PooledPostgresqlDatabase):
  def __init__(self, args):
    super(LoggingDatabase, self).__init__(
      database=args.pg_database, register_unicode=True, encoding=None,
      isolation_level=None, host=args.pg_host, user=args.pg_user, port=args.pg_port, password=args.pg_password,
      connection_factory=LoggingConnection
    )

  def _connect(self):
    conn = super(LoggingDatabase, self)._connect()
    conn.initialize(logger)
    return conn

#класс отвечающий за создания пулла сессий
#берем свободную и возвращаем назад
class ConnectionFactory:
  def __init__(self, open_fxn, close_fxn, create_db_fxn):
    self.open_fxn = open_fxn
    self.close_fxn = close_fxn
    self.create_db_fxn = create_db_fxn

  def getconn(self):
    return self.open_fxn()

  def putconn(self, conn):
    return self.close_fxn(conn)

  def create_db(self):
    return self.create_db_fxn()

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

    def create_db_sqlite():
      return PooledSqliteDatabase(args.sqlite_file)

    return ConnectionFactory(open_fxn=open_sqlite, close_fxn=close_sqlite, create_db_fxn=create_db_sqlite)
  else:
    #print('POSTGRE')
    def open_pg():
      return connect(f"postgres+pool://{args.pg_user}:{args.pg_password}@{args.pg_host}:{args.pg_port}/{args.pg_database}")

    def close_pg(conn):
      conn.close()

    def create_db_pg():
      return LoggingDatabase(args)

    return ConnectionFactory(open_fxn=open_pg, close_fxn=close_pg, create_db_fxn=create_db_pg)

connection_factory = create_connection_factory(parse_cmd_line())