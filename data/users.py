import sqlalchemy 
import datetime
from sqlalchemy import orm 
from . import db_session
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String) 
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) 

    image = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default='avatar.jpg') 
    
    email = sqlalchemy.Column(sqlalchemy.String, 
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)

    is_privated = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    news = orm.relation("News", back_populates='user')
'''
    def validate_email(self, email):
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email.data).first()
        if user:
            if user.id != self.id:
                raise ValidationError('Мыло занято')
'''
