from flask import redirect, render_template, url_for
from data import db_session
from flask_login import login_required, logout_user, login_user, current_user
from data.users import User
from forms import LoginForm, RegisterForm
from various import *


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/main_page/1")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        session = db_session.create_session()
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', form=form, title="Регистрация",
                                   current_user=current_user,
                                   message_password="Пароли не совпадают",
                                   style=url_for("static", filename="css/style.css"))
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, title="Регистрация",
                                   current_user=current_user,
                                   message_email="Почта уже используется",
                                   style=url_for("static", filename="css/style.css"))
        if session.query(User).filter(User.name == form.username.data).first():
            return render_template('register.html', form=form, title="Регистрация", current_user=current_user,
                                   message_name="Логин уже используется",
                                   style=url_for("static", filename="css/style.css"))
        user.name = form.username.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        session = db_session.create_session()
        session.add(user)
        session.commit()
        return redirect('/main_page/1')
    return render_template('register.html', form=form, title="Регистрация", current_user=current_user,
                           style=url_for("static", filename="css/style.css"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/main_page/1')
        user = session.query(User).filter(User.name == form.email.data).first()
        if user and user.hashed_password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/main_page/1')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, current_user=current_user, style=url_for("static", filename="css/style.css"))
    return render_template('login.html', form=form, title="Войти", current_user=current_user,
                           style=url_for("static", filename="css/style.css"))
