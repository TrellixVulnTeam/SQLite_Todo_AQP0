import sqlite3
from sqlite3 import Error

class TodosSQLite:

    def create_connection(self):
        try:
            self.conn = sqlite3.connect("database.db")
            return self.conn
        except Error as e:
            print(e)    
        return self.conn

    def all(self):
        with self.conn as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM todos")
        return cur.fetchall()
    
    def get(self, id):
        with self.conn as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM todos WHERE id={id}")
            row = cur.fetchone()
            dict = {"id": row[0], "title": row[1], "description": row[2], "done": row[3], "raing": row[4]}
        return dict
    
    def create(self, data):
        data.pop('csrf_token')
        with self.conn as conn:
            cur = conn.cursor()
            sql = """INSERT INTO todos (title, description, done, rating) VALUES (?,?,?,?)"""
            values = []
            for val in data.values():
                values.append(val)
            cur.execute(sql,values)
            conn.commit()
        return cur.lastrowid

    def update(self, id, data):
        data.pop('csrf_token')
        with self.conn as conn:
            cur = conn.cursor()
            parameters = [f"{k} = ?" for k in data.keys()]
            parameters = ", ".join(parameters)
            values = tuple(v for v in data.values())
            values += (id, )
            sql = f''' UPDATE todos
                        SET {parameters}
                        WHERE id = ?'''            
            try:
                cur.execute(sql, values)
                conn.commit()
            except sqlite3.OperationalError as e:
                print(e)
