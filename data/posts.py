from typing import Any

import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase, UserMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    creator_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    creator_surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    creator_login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    post_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    create_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False, default=datetime.datetime.now())
    text_content = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    file = sqlalchemy.Column(sqlalchemy.BLOB, default=None, nullable=True)
    is_liked = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    is_blog = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    is_training = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)
    is_recipe = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)

    def __repr__(self):
        return f'<User> {self.id} {self.post_name} {self.create_date}'
