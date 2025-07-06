from flask import Blueprint, jsonify, request
from app.dao.orders_dao import OrdersDAO

orders_routes = Blueprint('orders_routes', __name__)
orders_dao = OrdersDAO()

@orders_routes.route('/orders', methods=['GET'])
def GetOrders():
    """
    Endpoint to fetch all orders.
    """
    try:
        orders = orders_dao.GetOrders()
        if orders is not None:
            return jsonify(orders), 200
        else:
            return jsonify({"error": "No orders found"}), 404
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return jsonify({"error": str(e)}), 500

@orders_routes.route('/orders/<int:order_id>', methods=['GET'])
def GetOrderById(order_id):
    """
    Endpoint to fetch an order by its ID.
    """
    try:
        order = orders_dao.GetOrderById(order_id)
        if order:
            return jsonify(order), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        print(f"Error fetching order by ID: {e}")
        return jsonify({"error": str(e)}), 500

@orders_routes.route('/orders', methods=['POST'])
def CreateOrder():
    """
    Endpoint to create a new order.
    """
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        order_date = data.get('order_date')
        order_id = orders_dao.CreateOrder(customer_id, order_date)
        return jsonify({"order_id": order_id}), 201
    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({"error": str(e)}), 500