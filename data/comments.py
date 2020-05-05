import sqlalchemy
from .db_session import SqlAlchemyBase
import datetime
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user = orm.relation('User')
    topic = orm.relation('Topic')
