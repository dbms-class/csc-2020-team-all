from connect import create_connection_factory
from connect import parse_cmd_line


class Uploader(object):
    def __init__(self, args):
        self.connection_factory = create_connection_factory(args)

    def run_sql_script(self, filename):
        sql_file = open(filename)
        sql_as_string = sql_file.read()
        db = self.connection_factory.getconn()
        try:
            cur = db.cursor()
            cur.execute(sql_as_string)
            db.commit()
        finally:
            self.connection_factory.putconn(db)


if __name__ == '__main__':
    uploader = Uploader(parse_cmd_line())
    uploader.run_sql_script("project12.sql")
    uploader.run_sql_script("testdata.sql")
