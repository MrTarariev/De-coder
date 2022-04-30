import sqlite3
from database_management.user import User
import datetime


class DatabaseControl:
    def __init__(self, database_name):
        self.db_name = database_name
        self.user = None

    def set_user(self, name: str):
        self.user = User(name)
        if self.user.in_database(self.db_name):
            pass
        else:
            self.__add_user(name)

    def __add_user(self, name: str):
        connection = sqlite3.connect(self.db_name)
        connection.cursor().execute(
            f"INSERT INTO users_table(name) VALUES('{name}')"
        )
        connection.commit()
        connection.close()

    def get_spending(self, username: str = None, category: str = None,
                     day: str = None, month: str = None, year: str = None):
        if not username:
            username = self.user.name
        if day and not (month or year):
            date = f'{day}.{datetime.date.today().month}.' \
                   f'{datetime.date.today().year}'
        elif day and month and not year:
            date = f'{day}.{month}.{datetime.date.today().year}'
        elif day and month and year:
            date = '.'.join([day, month, year])
        elif not day and month and not year:
            date = f'%.{month}.{datetime.date.today().year}'
        elif not day and month and year:
            date = f'%.{month}.{year}'
        elif not day and not month and year:
            date = f'%.{year}'
        else:
            date = reversed(f'{datetime.date.today()}')

        connection = sqlite3.connect(self.db_name)

        if not category:
            query_result = connection.cursor().execute(
                f"""SELECT sum 
FROM main_table INNER JOIN users_table 
ON main_table.user_id = users_table.id 
INNER JOIN operation_types 
ON main_table.operation_type = operation_types.id 
WHERE operation_types.type == 'out' 
AND users_table.name = '{username}' 
AND main_table.date LIKE '{date}'"""
            ).fetchall()
        else:
            query_result = connection.cursor().execute(
                f"""SELECT sum 
FROM main_table INNER JOIN users_table 
ON main_table.user_id = users_table.id 
INNER JOIN operation_types 
ON main_table.operation_type = operation_types.id
INNER JOIN categories
ON main_table.category = categories.id 
WHERE operation_types.type == 'out' 
AND users_table.name = '{username}' 
AND main_table.date LIKE '{date}'
AND categories.category = '{category}'"""
            )
            connection.close()
        result = 0
        for line in query_result:
            result += line[0]
        return result

    def get_earnings(self, username: str = None, day: str = None,
                     month: str = None, year: str = None):
        if not username:
            username = self.user.name
        if day and not (month or year):
            date = f'{day}.{datetime.date.today().month}.' \
                   f'{datetime.date.today().year}'
        elif day and month and not year:
            date = f'{day}.{month}.{datetime.date.today().year}'
        elif day and month and year:
            date = '.'.join([day, month, year])
        elif not day and month and not year:
            date = f'%.{month}.{datetime.date.today().year}'
        elif not day and month and year:
            date = f'%.{month}.{year}'
        elif not day and not month and year:
            date = f'%.{year}'
        else:
            date = reversed(f'{datetime.date.today()}')

        connection = sqlite3.connect(self.db_name)

        query_result = connection.cursor().execute(
            f"""SELECT sum 
        FROM main_table INNER JOIN users_table 
        ON main_table.user_id = users_table.id 
        INNER JOIN operation_types 
        ON main_table.operation_type = operation_types.id 
        WHERE operation_types.type == 'in' 
        AND users_table.name = '{username}' 
        AND main_table.date LIKE '{date}'"""
        ).fetchall()
        connection.close()
        result = 0
        for line in query_result:
            result += line[0]
        return result

    def add_spending(self, summa: int, username: str = None,
                     category: int = 7):
        if username:
            self.set_user(username)
        connection = sqlite3.connect(self.db_name)
        connection.cursor().execute(
            f"""INSERT INTO 
main_table(user_id, date, operation_type, sum, category)
VALUES 
({self.user.id}, '{reversed(f'datetime.date.today()')}', 2, {summa}, 
{category})"""
        )
        connection.commit()
        connection.close()

    def add_earning(self, summa: int, username: str = None):
        if username:
            self.set_user(username)
        connection = sqlite3.connect(self.db_name)
        connection.cursor().execute(
            f"""INSERT INTO main_table(user_id, date, operation_type, sum)
VALUES ({self.user.id}, '{reversed(f'{datetime.date.today()}')}', 1, {summa})"""
        )
        connection.commit()
        connection.close()

    def get_category(self, category_id):
        connection = sqlite3.connect(self.db_name)
        result = connection.cursor().execute(
            f"""SELECT category FROM categories WHERE id = {category_id}"""
        ).fetchall()[0][0]
        connection.close()
        return result
