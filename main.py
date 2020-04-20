from flask import Flask, redirect
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from flask_login import login_user, current_user
from flask_login import login_required, logout_user, LoginManager

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


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def main_page():
    return render_template("base.html", title="Форум", current_user=current_user)


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
        user.name = form.username.data
        user.email = form.email.data
        user.hashed_password = form.password.data
        session = db_session.create_session()
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', form=form, title="Регистрация", current_user=current_user)


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
                               form=form, current_user=current_user)
    return render_template('login.html', form=form, title="Войти", current_user=current_user)


if __name__ == "__main__":
    db_session.global_init("db/blogs.sqlite")
    app.run(port=8080, host="127.0.0.1")

