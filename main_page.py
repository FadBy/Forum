from various import *
from flask import redirect, request, render_template, url_for
from flask_login import current_user
from data import db_session
from data.topics import Topic
from data.users import User
from math import ceil


@app.route("/")
def main():
    return redirect("/main_page/1")


@app.route("/main_page/<int:page>", methods=["GET", 'POST'])
def main_page(page):
    if request.method == "POST":
        return redirect("/main_page/" + request.form["btn"])
    max_topics = 10
    session = db_session.create_session()
    topics = session.query(Topic).all()
    length = len(topics)
    count_page = ceil(length / 10)
    topics.reverse()
    return render_template("main_page.html", title="Форум", current_user=current_user,
                           topics=topics, length=length, page=page, str=str, max_topics=max_topics,
                           count_page=count_page,
                           style=url_for("static", filename="css/style.css"))


@app.route("/profile/<name>")
def profile(name):
    session = db_session.create_session()
    user = session.query(User).filter(User.name == name).first()
    print(user)
    return render_template('profile.html', user=user, style=url_for("static", filename="css/style.css"),
                           title="Профиль " + user.name)
