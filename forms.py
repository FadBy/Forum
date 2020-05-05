from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('E-mail или Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repeat_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


class AddTopicForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = StringField('Описание', validators=[])
    submit = SubmitField('Создать')
