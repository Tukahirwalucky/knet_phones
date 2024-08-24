from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager  # Import JWTManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
mail = Mail()
cors =CORS()
socketio = SocketIO()
jwt = JWTManager()  # Initialize JWTManager
