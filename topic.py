from various import *
from forms import AddTopicForm
from data import db_session
from data.topics import Topic
from data.likes import Like
from data.comments import Comment
from flask import request, render_template, redirect
from flask_login import current_user
from requests import delete


@app.route("/add_topic", methods=['GET', 'POST'])
def add_topic():
    form = AddTopicForm()
    if form.validate_on_submit():
        topic = Topic()
        topic.title = form.title.data
        topic.description = request.form["description"]
        topic.user_id = current_user.id
        session = db_session.create_session()
        session.add(topic)
        session.commit()
        return redirect("/")
    return render_template("add_topic.html", style=style(), title="Создание темы", form=form)


@app.route("/topic/<int:id>", methods=['GET', 'POST'])
def topic(id):
    session = db_session.create_session()
    topic = session.query(Topic).filter(Topic.id == id).first()
    comments = session.query(Comment).filter(Comment.topic_id == id).all()
    comments.reverse()
    if current_user.is_authenticated:
        like = session.query(Like).filter(Like.topic_id == topic.id, Like.user_id == current_user.id).first()
        if like is None:
            like = False
        else:
            like = True
    else:
        like = False
    if request.method == 'POST':
        if request.form["btn"] == "send":
            comment = Comment()
            comment.user_id = current_user.id
            comment.topic_id = topic.id
            comment.text = request.form['write_comment']
            session.add(comment)
            session.commit()
            topic.comments += 1
            current_user.comments += 1
            session.commit()
            return redirect("/topic/" + str(id))
        elif request.form["btn"] == "like":
            if not like:
                like = Like()
                like.topic_id = topic.id
                like.user_id = current_user.id
                session.add(like)
                session.commit()
                topic.likes += 1
                current_user.likes += 1
                session.commit()
                like = True
            else:
                like = session.query(Like).filter(Like.user_id == current_user.id, Like.topic_id == topic.id).first()
                session.delete(like)
                session.commit()
                topic.likes -= 1
                current_user.likes -= 1
                session.commit()
                like = False
    return render_template("topic.html", style=style(), title=topic.title, current_user=current_user, topic=topic,
                           comments=comments, like=like)


@app.route("/delete_topic/<int:id>")
def delete_topic(id):
    delete("http://localhost:5000/api/topics/" + str(id))
    return redirect('/main_page/1')


@app.route("/delete_comment/<int:topic_id>/<int:comment_id>")
def delete_comment(topic_id, comment_id):
    delete("http://localhost:5000/api/comments/" + str(comment_id))
    return redirect("/topic/" + str(topic_id))
