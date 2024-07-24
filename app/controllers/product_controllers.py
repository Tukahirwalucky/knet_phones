# from flask import Blueprint, request, jsonify
# from app.models.product import Product
# from app.models.user import User
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.extensions import db
# import requests
# import base64

# product_bp = Blueprint('products', __name__, url_prefix='/api/v1/products')

# def encode_image_to_base64(image_binary):
#     return base64.b64encode(image_binary).decode('utf-8')

# @product_bp.route('/create', methods=['POST'])
# @jwt_required()
# def create_product():
#     try:
#         current_user_id = get_jwt_identity()
#         current_user = User.query.get(current_user_id)

#         if current_user.role != 'admin':
#             return jsonify({'error': 'Unauthorized access'}), 403

#         data = request.json
#         required_fields = ['name', 'price', 'stock', 'image']
#         if not all(field in data for field in required_fields):
#             return jsonify({'error': 'Missing required fields'}), 400

#         image_url = data.get('image')
#         if image_url:
#             image_response = requests.get(image_url)
#             image_binary = image_response.content
#             image_base64 = encode_image_to_base64(image_binary)
#         else:
#             return jsonify({'error': 'Image URL is required'}), 400

#         product = Product(
#             image=image_binary,
#             name=data['name'],
#             description=data.get('description', ''),
#             price=data['price'],
#             stock=data['stock'],
#             user_id=current_user_id
#         )

#         db.session.add(product)
#         db.session.commit()

#         return jsonify({
#             'message': 'Product created successfully',
#             'product': {
#                 'id': product.id,
#                 'image': image_base64,  # Return base64-encoded image
#                 'name': product.name,
#                 'description': product.description,
#                 'price': product.price,
#                 'stock': product.stock,
#                 'user_id': product.user_id,
#                 'created_at': product.created_at,
#                 'updated_at': product.updated_at
#             }
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @product_bp.route('/<int:product_id>', methods=['GET'])
# @jwt_required()
# def get_product_by_id(product_id):
#     try:
#         product = Product.query.get(product_id)
#         if not product:
#             return jsonify({'error': 'Product not found'}), 404

#         image_base64 = encode_image_to_base64(product.image)  # Encode image to base64

#         serialized_product = {
#             'id': product.id,
#             'image': image_base64,
#             'name': product.name,
#             'description': product.description,
#             'price': product.price,
#             'stock': product.stock,
#             'created_at': product.created_at,
#             'updated_at': product.updated_at
#         }

#         return jsonify(serialized_product), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @product_bp.route('/<int:product_id>', methods=['PUT'])
# @jwt_required()
# def update_product(product_id):
#     try:
#         current_user_id = get_jwt_identity()
#         current_user = User.query.get(current_user_id)

#         if current_user.role != 'admin':
#             return jsonify({'error': 'Unauthorized access'}), 403

#         data = request.json
#         product = Product.query.get(product_id)
#         if not product:
#             return jsonify({'error': 'Product not found'}), 404

#         product.name = data.get('name', product.name)
#         image_url = data.get('image')
#         if image_url:
#             image_response = requests.get(image_url)
#             product.image = image_response.content
#         product.description = data.get('description', product.description)
#         product.price = float(data.get('price', product.price))
#         product.stock = int(data.get('stock', product.stock))

#         db.session.commit()

#         return jsonify({
#             'message': 'Product updated successfully',
#             'product': {
#                 'id': product.id,
#                 'image': encode_image_to_base64(product.image),  # Return image as base64 encoded string
#                 'name': product.name,
#                 'description': product.description,
#                 'price': product.price,
#                 'stock': product.stock,
#                 'created_at': product.created_at,
#                 'updated_at': product.updated_at
#             }
#         }), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500

# @product_bp.route('/<int:product_id>', methods=['DELETE'])
# @jwt_required()
# def delete_product(product_id):
#     try:
#         current_user_id = get_jwt_identity()
#         current_user = User.query.get(current_user_id)

#         if current_user.role != 'admin':
#             return jsonify({'error': 'Unauthorized access'}), 403

#         product = Product.query.get(product_id)
#         if not product:
#             return jsonify({'error': 'Product not found'}), 404

#         db.session.delete(product)
#         db.session.commit()

#         return jsonify({'message': 'Product deleted successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': str(e)}), 500
from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
import requests
import base64

product_bp = Blueprint('products', __name__, url_prefix='/api/v1/products')

def encode_image_to_base64(image_binary):
    return base64.b64encode(image_binary).decode('utf-8')

@product_bp.route('/create', methods=['POST'])
@jwt_required()
def create_product():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if current_user.role != 'admin':
            return jsonify({'error': 'Unauthorized access'}), 403

        data = request.json
        required_fields = ['name', 'price', 'stock', 'image']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        image_url = data.get('image')
        if image_url:
            image_response = requests.get(image_url)
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
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

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
        return jsonify({'error': str(e)}), 500

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

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
        return jsonify({'error': str(e)}), 500
