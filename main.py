from flask import Flask, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.topics import Topic
from flask_login import login_required, logout_user, LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


class AddTopicForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = StringField('Описание', validators=[])
    submit = SubmitField('Создать')


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


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
    return render_template("add_topic.html", title="Создание темы", form=form,
                           style=url_for("static", filename="css/style.css"))


@app.route("/")
def main_page():
    session = db_session.create_session()
    topics = session.query(Topic).all()
    topics.reverse()
    return render_template("main_page.html", title="Форум", current_user=current_user, topics=topics, str=str,
                           style=url_for("static", filename="css/style.css"))


@app.route("/topic/<int:id>")
def topic(id):
    session = db_session.create_session()
    topic = session.query(Topic).filter(Topic.id == id).first()
    print(topic.user.name)
    return render_template("topic.html", title=topic.title, current_user=current_user, topic=topic,
                           style=url_for("static", filename="css/style.css"))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        session = db_session.create_session()
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
        return redirect('/')
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
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, current_user=current_user, style=url_for("static", filename="css/style.css"))
    return render_template('login.html', form=form, title="Войти", current_user=current_user,
                           style=url_for("static", filename="css/style.css"))


@app.route("/delete/<int:id>")
def delete(id):
    session = db_session.create_session()
    topic = session.query(Topic).filter(Topic.id == id).first()
    session.delete(topic)
    session.commit()
    return redirect('/')


if __name__ == "__main__":
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host="127.0.0.1")
