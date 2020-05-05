import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Like(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'likes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    topic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("topics.id"))
    user = orm.relation('User')
    topic = orm.relation('Topic')
