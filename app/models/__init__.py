from flask import Flask, jsonify, request
from flask_cors import CORS
from app.extensions import db, jwt, bcrypt
from app.controllers.user_controllers import user_bp
from app.controllers.product_controllers import product_bp
from app.controllers.order_controllers import order_bp
from app.controllers.refresh_token import refresh_bp
import logging

def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Configure CORS for the entire app
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Configure your app (database, JWT, etc.)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    app.register_blueprint(user_bp, url_prefix='/api/v1/users')
    app.register_blueprint(product_bp, url_prefix='/api/v1/products')
    app.register_blueprint(order_bp, url_prefix='/api/v1/orders')
    app.register_blueprint(refresh_bp)  # Register the refresh token blueprint

    # Define a before request handler for logging
    @app.before_request
    def log_request_info():
        app.logger.debug(f"Request Headers: {request.headers}")
        app.logger.debug(f"Request Body: {request.get_data()}")

    # Define a basic route to check if the server is up
    @app.route('/')
    def home():
        return 'Welcome to the API!'

    # Example route to test database connection
    @app.route('/test_db')
    def test_db():
        try:
            result = db.engine.execute('SELECT 1')
            return jsonify({'message': 'Database connection successful'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
