from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO


#App configurations

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ndidiwiiw8eyye72i2uyeheh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
chat_bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

server_socket = SocketIO(app)

def create_database(app):
	if not path.exists('Project2020/test.db'):
		db.create_all(app=app)

from .main.routes import main
from .users.routes import user

app.register_blueprint(main)
app.register_blueprint(user)