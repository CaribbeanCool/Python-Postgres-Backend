from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from dao import CustomersDAO

customers_routes = Blueprint("customers_routes", __name__)


@customers_routes.route("/customers", methods=["GET"])
@jwt_required()
def GetCustomers():
    """
    Endpoint to fetch all customers.
    """
    try:
        customers = CustomersDAO.GetCustomers()
        if customers is not None:
            return jsonify(customers), 200
        else:
            return jsonify({"error": "No customers found"}), 404
    except Exception as e:
        print(f"Error fetching customers: {e}")
        return jsonify({"error": str(e)}), 500


@customers_routes.route("/customers/<int:customer_id>", methods=["GET"])
def GetCustomerById(customer_id):
    """
    Endpoint to fetch a customer by its ID.
    """
    try:
        customer = CustomersDAO.GetCustomerById(customer_id)
        if customer:
            return jsonify(customer), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        print(f"Error fetching customer by ID: {e}")
        return jsonify({"error": str(e)}), 500


# @customers_routes.route('/customers', methods=['POST'])
# @jwt_required()
# def create_customer():
#     """
#     Endpoint to create a new customer.
#     """
#     try:
#         data = request.get_json()
#         name = data.get('name')
#         email = data.get('email')

#         if not name or not email:
#             return jsonify({"error": "Name and email are required"}), 400

#         customer_id = CustomersDAO.create_customer(name, email)
#         if customer_id:
#             return jsonify({"customer_id": customer_id}), 201
#         else:
#             return jsonify({"error": "Failed to create customer"}), 500
#     except Exception as e:
#         print(f"Error creating customer: {e}")
#         return jsonify({"error": str(e)}), 500
