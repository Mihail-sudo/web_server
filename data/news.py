import sqlalchemy 
from sqlalchemy import orm 
from .db_session import SqlAlchemyBase
import datetime
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin): 
    __tablename__ = 'news' 
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    news_tittle = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    news = sqlalchemy.Column(sqlalchemy.String, nullable=False) 
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    usered = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')