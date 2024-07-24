# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# import os

# load_dotenv()

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('config.Config')

#     # Initialize SQLAlchemy
#     db.init_app(app)

#     # Import models
#     with app.app_context():
#         from app.models import user, product, order

#     # Import blueprints
#     from app.routes import product_bp, user_bp, order_bp
   

#     # Register blueprints
#     app.register_blueprint(product_bp, url_prefix='/api/v1/products')
#     app.register_blueprint(user_bp, url_prefix='/api/v1/users')
#     app.register_blueprint(order_bp, url_prefix='/api/v1/orders')

#     return app
from flask import Flask
from app.extensions import db, mail, socketio
from app.routes import product_bp, user_bp, order_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)  # Initialize socketio if used

    # Register blueprints
    app.register_blueprint(product_bp, url_prefix='/api/v1/products')
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(order_bp, url_prefix='/api/v1/orders')

    return app
