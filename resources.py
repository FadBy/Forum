from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data import db_session
from data.topics import Topic
from data.comments import Comment
from data.users import User
from data.likes import Like
from flask_login import current_user


def abort_if_not_found(category, id):
    session = db_session.create_session()
    category = session.query(category).get(id)
    if not category:
        abort(404, message=f"{id} not found")


class TopicResource(Resource):
    def get(self, topic_id):
        abort_if_not_found(Topic, topic_id)
        session = db_session.create_session()
        topic = session.query(Topic).get(topic_id)
        comments = session.query(Comment).filter(Comment.topic_id == topic.id).all()
        return jsonify({'topic': topic.to_dict(
            only=('id', 'title', 'description', 'user_id', 'created_date', "likes", "comments")), "user": topic.user.to_dict(
            only=('id', 'name', 'email')),
            "comments": [comment.to_dict(only=("user_id", "text", "created_date")) for comment in comments]})

    def delete(self, topic_id):
        abort_if_not_found(Topic, topic_id)
        session = db_session.create_session()
        topic = session.query(Topic).get(topic_id)
        comments = session.query(Comment).filter(Comment.topic_id == topic.id).all()
        likes = session.query(Like).filter(Like.topic_id == topic.id).all()
        for i in comments:
            i.user.comments -= 1
            session.delete(i)
        for i in likes:
            i.user.likes -= 1
            session.delete(i)
        session.delete(topic)
        session.commit()
        return jsonify({'success': 'OK'})


class TopicListResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', required=True)
        self.parser.add_argument('description', required=True)
        self.parser.add_argument('user_id', required=True, type=int)

    def get(self):
        session = db_session.create_session()
        news = session.query(Topic).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in news]})

    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        topic = Topic(
            title=args['title'],
            description=args['description'],
            user_id=args['user_id']
        )
        session.add(topic)
        session.commit()
        return jsonify({'success': 'OK'})


class UserResource(Resource):
    def get(self, user_id):
        abort_if_not_found(User, user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({"user": user.to_dict(only=("id", "name", "email", "created_date"))})


class LikeResource(Resource):
    def get(self, topic_id, user_id):
        session = db_session.create_session()
        like = session.query(Like).filter(Like.topic_id == topic_id, Like.user_id == user_id).first()
        if like is None:
            return jsonify({"like": None})
        return jsonify({"like": like.to_dict("id", "user_id", "topic_id")})

    def delete(self, topic_id, user_id):
        abort_if_not_found(Topic, topic_id)
        abort_if_not_found(User, user_id)
        session = db_session.create_session()
        like = session.query(Like).filter(Like.topic_id == topic_id, Like.user_id == user_id).first()
        session.delete(like)
        session.commit()
        return jsonify({'success': 'OK'})

    def post(self, topic_id, user_id):
        session = db_session.create_session()
        if current_user.id == user_id:
            like = Like(
                topic_id=topic_id,
                user_id=user_id
            )
            session.add(like)
            session.commit()
            user = like.user
            topic = like.topic
            user.likes += 1
            topic.likes += 1
            session.commit()
            return jsonify({'success': 'OK'})
        return jsonify({"result": "not enough rights"})


class CommentResource(Resource):
    def get(self, comment_id):
        abort_if_not_found(Comment, comment_id)
        session = db_session.create_session()
        comment = session.query(Comment).get(comment_id)
        return jsonify({"comment": comment.to_dict("id", "text", "user_id", "topic_id")})

    def delete(self, comment_id):
        abort_if_not_found(Comment, comment_id)
        session = db_session.create_session()
        comment = session.query(Comment).get(comment_id)
        comment.topic.comments -= 1
        comment.user.comments -= 1
        print(comment_id)
        session.delete(comment)
        session.commit()
        return jsonify({'success': 'OK'})


class CommentListResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', required=True, type=int)
        self.parser.add_argument('text', required=True)

    def post(self, topic_id):
        args = self.parser.parse_args()
        session = db_session.create_session()
        comment = Comment(
            user_id=args['user_id'],
            topic_id=topic_id,
            text=args['text']
        )
        session.add(comment)
        session.commit()
        comment.user.comments += 1
        comment.topic.comments += 1
        return jsonify({'success': 'OK'})


