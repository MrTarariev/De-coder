import sqlite3
from database_management.user import User


class DatabaseControl:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.user = None

    def set_user(self, name: str):
        self.user = User(name)
        if self.user.in_database(self.connection):
            pass
        else:
            self.add_user(name)

    def add_user(self, name: str):
        self.connection.cursor().execute(
            f"'INSERT INTO users(name) VALUES ('{name}')'"
        )

    def get_spending(self):
        print('пока не работает')

    def get_earnings(self):
        print('пока не работает')
