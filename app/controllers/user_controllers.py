
from flask import Blueprint, request, jsonify
from app.models.user import User
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, generate_password_hash
from app.extensions import bcrypt, db
import logging

user_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@user_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        print(f"Received user data: {data}")  # Print received data

        required_fields = ['name', 'email', 'password', 'address', 'phone_number']
        if not all(data.get(field) for field in required_fields):
            print(f"Missing required fields: {', '.join(field for field in required_fields if not data.get(field))}")
            return jsonify({'error': 'All fields are required'}), 400

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            print(f"Email {data['email']} already exists")
            return jsonify({'error': 'Email already exists'}), 409

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            address=data['address'],
            phone_number=data['phone_number'],
            role=data.get('role', 'customer')
        )

        print(f"Created new user object: {new_user}")  # Print the created user object

        db.session.add(new_user)
        db.session.commit()

        response_user = {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
            'phone_number': new_user.phone_number,
            'address': new_user.address,
            'role': new_user.role,
            'created_at': new_user.created_at,
            'updated_at': new_user.updated_at
        }

        print(f"Response data: {response_user}")  # Print the response data

        return jsonify({
            'message': f'User {new_user.name} has been successfully created',
            'user': response_user
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {str(e)}")  # Print the exception message
        return jsonify({'error': 'An error occurred during registration'}), 500

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
            logging.debug(f"User {user.id} logged in successfully.")
            return jsonify({'access_token': access_token, 'user_id': user.id}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
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
        return jsonify({'error': str(e)}), 500
