from typing import Any

import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, UserMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    post_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("posts.id"))
    post = orm.relationship('Post')
    author_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    author_login = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    comment_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return f'<Comment> {self.id} {self.text} {self.comment_date}'