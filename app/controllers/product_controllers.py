from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.product import Product
from flask_cors import CORS
from app.models.user import User
from app.extensions import db
from flask_cors import cross_origin
import requests
import base64
import re

product_bp = Blueprint('products', __name__, url_prefix='/api/v1/products')

# Enable CORS for the entire blueprint
CORS(product_bp, resources={r"/api/v1/products/*": {"origins": "http://localhost:3000"}})

def encode_image_to_base64(image_binary):
    """Encode binary image data to a base64 string."""
    if not image_binary:
        return None
    return base64.b64encode(image_binary).decode('utf-8')

def parse_price(price_str):
    """Helper function to parse price from a string with currency symbols and commas."""
    try:
        cleaned_price = re.sub(r'[^\d.]', '', price_str)
        return float(cleaned_price)
    except ValueError:
        raise ValueError('Invalid price format')

@product_bp.route('/add', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin(origins="http://localhost:3000")
def add_product():
    

    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        name = data.get('name')
        price_str = data.get('price')
        image_url = data.get('image')
        description = data.get('description')
        stock = data.get('stock')

        if not name or not price_str or not image_url or not description or stock is None:
            return jsonify({'message': 'Name, price, image URL, description, and stock are required'}), 400

        try:
            price = parse_price(price_str)
            if price <= 0:
                raise ValueError('Price must be greater than zero.')
        except ValueError as ve:
            return jsonify({'message': str(ve)}), 400

        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            return jsonify({'message': 'Failed to fetch image from URL'}), 400
        image_binary = image_response.content

        product = Product(
            name=name,
            description=description,
            price=price,
            image=image_binary,
            stock=stock,
            user_id=current_user_id
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'message': 'Product added successfully',
            'product': {
                'id': product.id,
                'image': encode_image_to_base64(product.image),
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'created_at': product.created_at,
                'updated_at': product.updated_at
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding product: {str(e)}")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

# Other routes...



@product_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_products():
    try:
        products = Product.query.all()
        if not products:
            return jsonify([]), 200  # Return empty array if no products

        serialized_products = []
        for product in products:
            image_base64 = encode_image_to_base64(product.image)
            serialized_products.append({
                'id': product.id,
                'image': image_base64,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'created_at': product.created_at,
                'updated_at': product.updated_at
            })

        return jsonify(serialized_products), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching products: {str(e)}")
        return jsonify({'error': str(e)}), 422  # Use 422 to match the client-side error code

@product_bp.route('/create', methods=['POST'])
@jwt_required()
def create_product():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        required_fields = ['name', 'price', 'stock', 'image']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        image_url = data.get('image')
        if image_url:
            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                return jsonify({'error': 'Failed to fetch image from URL'}), 400
            image_binary = image_response.content
            image_base64 = encode_image_to_base64(image_binary)
        else:
            return jsonify({'error': 'Image URL is required'}), 400

        product = Product(
            image=image_binary,
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            stock=data['stock'],
            user_id=current_user_id
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            'message': 'Product created successfully',
            'product': {
                'id': product.id,
                'image': image_base64,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'user_id': product.user_id,
                'created_at': product.created_at,
                'updated_at': product.updated_at
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        image_base64 = encode_image_to_base64(product.image)

        serialized_product = {
            'id': product.id,
            'image': image_base64,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock,
            'created_at': product.created_at,
            'updated_at': product.updated_at
        }

        return jsonify(serialized_product), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching product by ID: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product.name = data.get('name', product.name)
        image_url = data.get('image')
        if image_url:
            image_response = requests.get(image_url)
            if image_response.status_code != 200:
                return jsonify({'error': 'Failed to fetch image from URL'}), 400
            product.image = image_response.content
        product.description = data.get('description', product.description)
        product.price = float(data.get('price', product.price))
        product.stock = int(data.get('stock', product.stock))

        db.session.commit()

        return jsonify({
            'message': 'Product updated successfully',
            'product': {
                'id': product.id,
                'image': encode_image_to_base64(product.image),
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'stock': product.stock,
                'created_at': product.created_at,
                'updated_at': product.updated_at
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'error': 'User not found'}), 404

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting product: {str(e)}")
        return jsonify({'error': str(e)}), 500
