import sqlite3


class User:
    def __init__(self, name: str):
        self.name = name
        self.id = None

    def in_database(self, database: sqlite3.Connection):
        result = database.cursor().execute(
            f"SELECT id FROM users_table WHERE name = '{self.name}'"
        ).fetchall()
        if result:
            self.id = result
            return True
        return False

