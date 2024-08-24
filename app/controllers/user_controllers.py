from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from app.models.user import User
from app.extensions import bcrypt, db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create a Blueprint
user_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        address = data.get('address')
        phone_number = data.get('phone_number')
        agree_to_terms = data.get('agreeToTerms')

        # Validate input
        if not all([name, email, password, address, phone_number, agree_to_terms]):
            return jsonify({'error': 'All fields are required'}), 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists'}), 400

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user
        new_user = User(name=name, email=email, password=hashed_password, address=address, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        logging.error(f'Error creating user: {e}', exc_info=True)
        return jsonify({'error': 'An error occurred during registration'}), 500

# Ensure the other routes are similarly defined within the same blueprint


@user_bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token, 'user_id': user.id}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        logging.error(f"An error occurred during login: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@user_bp.route('/edit/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        logged_in_user = User.query.filter_by(id=current_user_id).first()

        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        if logged_in_user.role != 'admin' and user.id != current_user_id:
            return jsonify({'error': 'You are not authorized to update user details'}), 403

        data = request.get_json()

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.address = data.get('address', user.address)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.role = data.get('role', user.role)

        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                return jsonify({'error': 'Password must have at least 6 characters'}), 400
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')

        db.session.commit()

        return jsonify({
            'message': f"{user.name}'s details have been successfully updated",
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'address': user.address,
                'role': user.role,
                'updated_at': user.updated_at,
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"An error occurred during user update: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@user_bp.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        logged_in_user = User.query.filter_by(id=current_user_id).first()

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if logged_in_user.role != 'admin':
            return jsonify({'error': 'You are not authorized to delete this user'}), 403

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"An error occurred during user deletion: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@user_bp.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        if user:
            serialized_user = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'address': user.address,
                'role': user.role,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            return jsonify({'user': serialized_user}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        logging.error(f"An error occurred during current user retrieval: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


