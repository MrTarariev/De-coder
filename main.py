# так выглядит вызов моего ORM в основной программе (Караму на заметку)

from database_management.my_orm_base import DatabaseControl

database = DatabaseControl('database_management/money_database.db')
database.set_user('username')
database.get_spending()  # print('пока не работает')
