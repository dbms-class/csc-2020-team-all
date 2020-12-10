from connect import create_connection_factory
from connect import parse_cmd_line


class Uploader(object):
    def __init__(self, args):
        self.connection_factory = create_connection_factory(args)

    def run_sql_script(self, filename):
        with open(filename, 'r') as sql_file:
            sql_as_string = sql_file.read()

        with self.connection_factory.conn() as db:
            cur = db.cursor()
            cur.execute(sql_as_string)
            db.commit()


if __name__ == '__main__':
    uploader = Uploader(parse_cmd_line())
    uploader.run_sql_script("project8.sql")
    uploader.run_sql_script("testdata.sql")
