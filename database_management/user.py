import sqlite3


class User:
    def __init__(self, name: str):
        self.name = name
        self.id = None

    def in_database(self, database: str):
        connection = sqlite3.connect(database)
        result = connection.cursor().execute(
            f"SELECT id FROM users_table WHERE name = '{self.name}'"
        ).fetchall()[0][0]
        connection.close()
        if result:
            self.id = result
            return True
        return False
