# from flask import Blueprint, request, jsonify, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from flask_mail import Message
# from app.models.order import Order
# from app.models.product import Product
# from app.extensions import db, mail

# order_bp = Blueprint('orders', __name__, url_prefix='/api/v1/orders')

# @order_bp.route('/place', methods=['POST'])
# @jwt_required()  # Ensure the user is authenticated
# def place_order():
#     try:
#         data = request.get_json()
#         email = data.get('email')
#         product_id = data.get('product_id')
#         quantity = data.get('quantity')
        
#         if not email or not product_id or quantity is None:
#             return jsonify({'message': 'Email, product ID, and quantity are required'}), 400

#         # Look up the product by ID
#         product = Product.query.get(product_id)
#         if not product:
#             return jsonify({'message': 'Product not found'}), 404
        
#         # Validate quantity
#         if quantity <= 0:
#             return jsonify({'message': 'Quantity must be greater than zero'}), 400
#         if quantity > product.stock:
#             return jsonify({'message': 'Insufficient stock available'}), 400

#         # Calculate total price
#         total_price = product.price * quantity

#         # Create the order
#         order = Order(
#             user_id=get_jwt_identity(),  # Assuming the current user's ID is used
#             product_id=product_id,
#             quantity=quantity,
#             total_price=total_price,
#             status='pending'  # Initial status of the order
#         )
        
#         # Update product stock
#         product.stock -= quantity

#         # Save the order and update product stock
#         db.session.add(order)
#         db.session.commit()

#         # Comment out email sending logic
#         # msg = Message('Order Confirmation', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
#         # msg.body = (
#         #     f"Thank you for your order!\n\n"
#         #     f"Product: {product.name}\n"
#         #     f"Price: ${product.price}\n"
#         #     f"Quantity: {quantity}\n"
#         #     f"Total Price: ${total_price}\n"
#         #     f"Description: {product.description}\n\n"
#         #     f"Your order has been placed successfully. The status of your order is '{order.status}'."
#         # )
#         # mail.send(msg)

#         # Emit a WebSocket event to notify the user
#         socketio.emit('new_order', {
#             'message': 'A new order has been placed',
#             'order': {
#                 'id': order.id,
#                 'product_id': product_id,
#                 'quantity': quantity,
#                 'total_price': total_price,
#                 'status': order.status
#             }
#         }, namespace='/user', room=get_jwt_identity())

#         return jsonify({
#             'message': 'Order placed successfully',
#             'order': {
#                 'id': order.id,
#                 'product_id': product_id,
#                 'quantity': quantity,
#                 'total_price': total_price,
#                 'status': order.status
#             }
#         }), 201

#     except Exception as e:
#         current_app.logger.error(f"Error placing order: {str(e)}")
#         return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500

# # Ensure the app is created and the Blueprint is registered in your main application file
# if __name__ == '__main__':
#     from app.controllers import create_app, socketio
#     app = create_app()
#     app.register_blueprint(order_bp)
#     socketio.run(app, debug=True)
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message
from app.models.order import Order
from app.models.product import Product
from app.extensions import db, mail
from app.extensions import socketio  # Import socketio

order_bp = Blueprint('orders', __name__, url_prefix='/api/v1/orders')

@order_bp.route('/place', methods=['POST'])
@jwt_required()
def place_order():
    try:
        data = request.get_json()
        email = data.get('email')
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        
        if not email or not product_id or quantity is None:
            return jsonify({'message': 'Email, product ID, and quantity are required'}), 400

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        if quantity <= 0:
            return jsonify({'message': 'Quantity must be greater than zero'}), 400
        if quantity > product.stock:
            return jsonify({'message': 'Insufficient stock available'}), 400

        total_price = product.price * quantity

        order = Order(
            user_id=get_jwt_identity(),
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status='pending'
        )
        
        product.stock -= quantity

        db.session.add(order)
        db.session.commit()

        # Commented out email sending logic
        # msg = Message('Order Confirmation', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
        # msg.body = (
        #     f"Thank you for your order!\n\n"
        #     f"Product: {product.name}\n"
        #     f"Price: ${product.price}\n"
        #     f"Quantity: {quantity}\n"
        #     f"Total Price: ${total_price}\n"
        #     f"Description: {product.description}\n\n"
        #     f"Your order has been placed successfully. The status of your order is '{order.status}'."
        # )
        # mail.send(msg)

        # Emit a WebSocket event to notify the user
        socketio.emit('new_order', {
            'message': 'A new order has been placed',
            'order': {
                'id': order.id,
                'product_id': product_id,
                'quantity': quantity,
                'total_price': total_price,
                'status': order.status
            }
        }, namespace='/user', room=get_jwt_identity())

        return jsonify({
            'message': 'Order placed successfully',
            'order': {
                'id': order.id,
                'product_id': product_id,
                'quantity': quantity,
                'total_price': total_price,
                'status': order.status
            }
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error placing order: {str(e)}")
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500
