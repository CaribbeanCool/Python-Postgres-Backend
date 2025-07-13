from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from dao import ProductsDAO

products_routes = Blueprint("products_routes", __name__)


@products_routes.route("/products", methods=["GET"])
def GetProducts():
    """
    Endpoint to fetch all products.
    """
    try:
        products = ProductsDAO.GetProducts()
        if products is not None:
            return jsonify(products), 200
        else:
            return jsonify({"error": "Failed to fetch products"}), 500
    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products/<int:product_id>", methods=["GET"])
def GetProductById(product_id):
    """
    Endpoint to fetch a product by its ID.
    """
    try:
        product = ProductsDAO.GetProductById(product_id)
        if product:
            return jsonify(product), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        print(f"Error fetching product by ID: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products", methods=["POST"])
@jwt_required()
def CreateProduct():
    """
    Endpoint to create a new product.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        product_name = data.get("product_name")
        unit = data.get("unit")
        price = data.get("price")

        if not product_name or not unit or not price:
            return jsonify({"error": "Product Name, Unit and Price are required"}), 400

        product_id = ProductsDAO.CreateProduct(product_name, unit, price)
        if product_id:
            return jsonify(
                {"product_id": product_id, "message": "Product created successfully"}
            ), 201
        else:
            return jsonify({"error": "Failed to create product"}), 500
    except Exception as e:
        print(f"Error creating product: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def UpdateProduct(product_id):
    """
    Endpoint to update an existing product.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        cat_id = data.get("category_id")
        unit = data.get("unit")
        price = data.get("price")

        if not cat_id or not unit or not price:
            return jsonify({"error": "Category Id, Unit and Price are required"}), 400

        updated_product_id = ProductsDAO.UpdateProduct(product_id, cat_id, unit, price)
        if updated_product_id:
            return jsonify(
                {
                    "product_id": updated_product_id,
                    "message": "Product updated successfully",
                }
            ), 200
        else:
            return jsonify({"error": "Product not found or failed to update"}), 404
    except Exception as e:
        print(f"Error updating product: {e}")
        return jsonify({"error": str(e)}), 500


@products_routes.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
def DeleteProduct(product_id):
    """
    Endpoint to delete a product.
    """
    try:
        deleted_product_id = ProductsDAO.DeleteProduct(product_id)
        if deleted_product_id:
            return jsonify(
                {
                    "product_id": deleted_product_id,
                    "message": "Product deleted successfully",
                }
            ), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        print(f"Error deleting product: {e}")
        return jsonify({"error": str(e)}), 500
