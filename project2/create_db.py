from connect import create_connection_factory
from connect import parse_cmd_line

def add_data(connection_factory, filename):
  #используем contextmanager, который сам в конце возращает сессию в пул
  with connection_factory.conn() as db:
    cur = db.cursor()
    file = open(filename)
    cur.execute(file.read())
    file.close()
    db.commit()

if __name__ == '__main__':
  connection_factory = create_connection_factory(parse_cmd_line())
  
  # добавляем все таблички
  add_data(connection_factory, "project2.sql")
    
  # добавляем данные для тестировки
  add_data(connection_factory, "init_db.sql")