import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("./todo_list.db")
        self.connection.row_factory = sqlite3.Row

    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor

    def close(self):
        self.connection.close()