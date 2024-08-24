from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
import logging

refresh_bp = Blueprint('refresh', __name__, url_prefix='/api/v1/refresh-token')

@refresh_bp.route('', methods=['POST'])
@jwt_required(refresh=True)  # Use jwt_required with refresh=True to get refresh tokens
def refresh_token():
    try:
        current_user_id = get_jwt_identity()
        # Create a new access token
        access_token = create_access_token(identity=current_user_id)
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        logging.error(f"An error occurred during token refresh: {str(e)}")
        return jsonify({'error': 'An error occurred during token refresh'}), 500
