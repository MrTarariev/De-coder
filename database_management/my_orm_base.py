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
            self.__add_user(name)

    def __add_user(self, name: str):
        self.connection.cursor().execute(
            f"'INSERT INTO users(name) VALUES ('{name}')'"
        )

    def get_spending(self, username: str = None, day: str = None,
                     month: str = None, year: str = None):
        if not username:
            username = self.user.name
        if day and not (month or year):
            date = f'{day}.%'
        elif day and month and not year:
            date = f'{day}.{month}.%'
        elif day and month and year:
            date = '.'.join([day, month, year])
        elif not day and month and not year:
            date = f'%.{month}.%'
        elif not day and month and year:
            date = f'%.{month}.{year}'
        elif not day and not month and year:
            date = f'%.{year}'
        else:
            date = '%'

        query_result = self.connection.cursor().execute(
            f"""SELECT sum 
FROM main_table INNER JOIN users_table 
ON main_table.user_id = users_table.id 
INNER JOIN operation_types 
ON main_table.operation_type = operation_types.id 
WHERE operation_types.type == 'out' 
AND users_table.name = '{username}' 
AND main_table.date LIKE '{date}'"""
        ).fetchall()
        result = 0
        for line in query_result:
            result += line[0]
        return result

    def get_earnings(self, username: str = None, day: str = None,
                     month: str = None, year: str = None):
        if not username:
            username = self.user.name
        if day and not (month or year):
            date = f'{day}.%'
        elif day and month and not year:
            date = f'{day}.{month}.%'
        elif day and month and year:
            date = '.'.join([day, month, year])
        elif not day and month and not year:
            date = f'%.{month}.%'
        elif not day and month and year:
            date = f'%.{month}.{year}'
        elif not day and not month and year:
            date = f'%.{year}'
        else:
            date = '%'

        query_result = self.connection.cursor().execute(
            f"""SELECT sum 
        FROM main_table INNER JOIN users_table 
        ON main_table.user_id = users_table.id 
        INNER JOIN operation_types 
        ON main_table.operation_type = operation_types.id 
        WHERE operation_types.type == 'in' 
        AND users_table.name = '{username}' 
        AND main_table.date LIKE '{date}'"""
        ).fetchall()
        result = 0
        for line in query_result:
            result += line[0]
        return result
