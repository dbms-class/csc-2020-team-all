# encoding: UTF-8

## Веб сервер
import cherrypy
import cherrypy_cors

from connect import parse_cmd_line
from connect import create_connection
from static import index


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    @cherrypy.expose
    def drop(self, table):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute(f'DROP TABLE {table}')
        return 'Done'

    @cherrypy.expose
    def fill(self):
        script = ''
        with open('../project8/project8.sql') as ddl:
            script = '\n'.join(list(map(str.rstrip, ddl.readlines())))
        if script == '':
            return 'Failed to read file'
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute(script)
        return 'Done'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def apartments(self, country_id=None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query = f'SELECT id, name, address, country_id FROM Apartments'
            if country_id is not None:
                query += f' WHERE country_id = {country_id}'
            cur.execute(query)
            return list(map(
                lambda apartment: {
                    'id': apartment[0], 'name': apartment[1],
                    'address': apartment[2], 'country_id': apartment[3]
                },
                cur.fetchall()
            ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def countries(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query = 'SELECT id, name FROM Countries'
            cur.execute(query)
            return list(map(
                lambda country: {'id': country[0], 'name': country[1]},
                cur.fetchall()
            ))

    @cherrypy.expose
    def update_price(self, apartment_id, week, price):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query = f'UPDATE Prices SET price = {price} WHERE apartment_id = {apartment_id} and week = {week}'
            cur.execute(query)
        return 'Done'
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_price(self, country_id, week, max_price=None, bed_count=None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            query_pattern = '''
            SELECT Apartments.id, name, bed_count, week, price 
            FROM Apartments join Prices 
                on Apartments.id = Prices.apartment_id 
            WHERE country_id = {0} and week = {1}'''
            query = query_pattern.format(country_id, week)
            
            if max_price is not None:
                query += f' and price <= {max_price}'
            if bed_count is not None:
                query += f' and bed_count >= {bed_count}'
            
            cur.execute(query)
            return list(map(
                lambda apartment: {
                    'id': apartment[0], 
                    'name': apartment[1],
                    'bed_count': apartment[2],
                    'week': apartment[3],
                    'price': apartment[4]
                },
                cur.fetchall()
            ))

def run():
    cherrypy_cors.install()
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
    })
    config = {
        '/': {
            'cors.expose.on': True,
        },
    }
    cherrypy.quickstart(App(parse_cmd_line()), config=config)


if __name__ == '__main__':
    run()
