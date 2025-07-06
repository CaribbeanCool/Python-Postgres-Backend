from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.dao.products_dao import ProductsDAO

products_routes = Blueprint("products_routes", __name__)
products_dao = ProductsDAO()


@products_routes.route("/products", methods=["GET"])
@jwt_required()
def GetProducts():
    """
    Endpoint to fetch all products.
    """
    try:
        products = products_dao.GetProducts()
        if products is not None:
            return jsonify(products), 200
        else:
            return jsonify({"error": "No products found"}), 404
    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products/<int:product_id>", methods=["GET"])
def GetProductById(product_id):
    """
    Endpoint to fetch a product by its ID.
    """
    try:
        product = products_dao.GetProductById(product_id)
        if product:
            return jsonify(product), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        print(f"Error fetching product by ID: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products", methods=["POST"])
def CreateProduct():
    """
    Endpoint to create a new product.
    """
    try:
        data = request.get_json()
        product_name = data.get("product_name")
        unit = data.get("unit")
        price = data.get("price")

        if not product_name or not unit or not price:
            return jsonify({"error": "Product Name, Unit and Price are required"}), 400

        product_id = products_dao.CreateProduct(product_name, unit, price)
        if product_id:
            return jsonify({"product_id": product_id}), 201
        else:
            return jsonify({"error": "Failed to create product"}), 500
    except Exception as e:
        print(f"Error creating product: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products/<int:product_id>", methods=["PUT"])
def UpdateProduct(product_id):
    try:
        data = request.get_json()
        cat_id = data.get("category_id")
        unit = data.get("unit")
        price = data.get("price")

        if not cat_id or not unit or not price:
            return jsonify({"error": "Category Id, Unit and Price are required"}), 400

        product = products_dao.UpdateProduct(product_id, cat_id, unit, price)
        if product:
            return jsonify(product), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        print(f"Error updating product: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products/<int:product_id>", methods=["DELETE"])
def DeleteProduct(product_id):
    try:
        product = products_dao.DeleteProduct(product_id)
        if product:
            return jsonify(product), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        print(f"Error deleting product: {e}")
        return jsonify({"error": str(e)}), 500
