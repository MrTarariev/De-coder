import datetime
import sqlalchemy
from kind_of_ORM import SqlAlchemyBase


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)


class OperationTypes(SqlAlchemyBase):
    __tablename__ = 'operation_types'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True, nullable=False, unique=True)
    type = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)


class MainTable(SqlAlchemyBase):
    __tablename__ = 'main_table'

    operation_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                                     autoincrement=True, nullable=False,
                                     unique=True)
    user_id = sqlalchemy.Column(sqlalchemy.INT,
                                sqlalchemy.ForeignKey('user.name'),
                                nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DATE, nullable=False,
                             default=datetime.date.today)
    operation_type = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey(
                                           'operation_types.type'
                                       ),
                                       nullable=False)
    sum = sqlalchemy.Column(sqlalchemy.INT, nullable=False)
