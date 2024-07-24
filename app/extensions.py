from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask import Blueprint
#from flask_socketio import SocketIO

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
#bp = Blueprint('main',__name__)
#socketio = SocketIO()


def init_app(app):
    mail.init_app(app)

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_socketio import SocketIO  # Add SocketIO import

db = SQLAlchemy()
mail = Mail()
socketio = SocketIO()  # Initialize SocketIO
