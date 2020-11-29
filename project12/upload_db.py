from connect import create_connection
from connect import parse_cmd_line


class Uploader(object):
    def __init__(self, args):
        self.args = args

    def run_sql_script(self, filename):
        sql_file = open(filename)
        sql_as_string = sql_file.read()
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute(sql_as_string)


if __name__ == '__main__':
    uploader = Uploader(parse_cmd_line())
    uploader.run_sql_script("project12.sql")
    uploader.run_sql_script("testdata.sql")
