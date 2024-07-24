from flask import Flask
from app.extensions import db, bcrypt
from app.routes import product_bp, user_bp, order_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize SQLAlchemy
    db.init_app(app)

    # Import models
    with app.app_context():
        from app.models import user, product, order
        db.create_all()  # Create database tables if they don't exist

    # Register blueprints
    app.register_blueprint(product_bp, url_prefix='/api/v1/products')
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(order_bp, url_prefix='/api/v1/orders')

    # Print URL map for debugging
    with app.app_context():
        print(app.url_map)

    return app
