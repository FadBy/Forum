from flask import Flask, url_for
from flask_login import LoginManager
from flask_restful import Api

def style():
    return url_for("static", filename="css/style.css")


app = Flask(__name__)
api = Api(app)
login_manager = LoginManager()
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'