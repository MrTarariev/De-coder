# так выглядит вызов моего ORM в основной программе (Караму на заметку)

from database_management.my_orm_base import DatabaseControl

database = DatabaseControl('database_management/money_database.db')
database.set_user('username')
print(database.get_spending())  # получаем расходы за сегодня
# можно дополнительно указать имя пользователя и дату
# вместо значений по умолчанию
# ничего не пишет, так как в базе пока нет расходов

print(database.get_earnings())  # получаем доходы за сегодня
# или за указанную дату для пользователя

database.add_spending(800)  # обязательный параметр - сумма
# необязательные: имя пользователя, категория расходов (по умолчанию "Другое")
