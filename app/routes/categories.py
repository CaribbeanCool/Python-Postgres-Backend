from flask import Blueprint, jsonify, request
from app.dao import CategoriesDAO

categories_routes = Blueprint("categories_routes", __name__)
categories_dao = CategoriesDAO()


@categories_routes.route("/categories", methods=["GET"])
def GetCategories():
    """
    Endpoint to fetch all categories.
    """
    try:
        categories = categories_dao.GetCategories()
        if categories is not None:
            return jsonify(categories), 200
        else:
            return jsonify({"error": "Failed to fetch categories"}), 500
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return jsonify({"error": str(e)}), 500


@categories_routes.route("/categories/<int:category_id>", methods=["GET"])
def GetCategoryById(category_id):
    """
    Endpoint to fetch a category by its ID.
    """
    try:
        category = categories_dao.GetCategoryById(category_id)
        if category:
            return jsonify(category), 200
        else:
            return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        print(f"Error fetching category: {e}")
        return jsonify({"error": str(e)}), 500


@categories_routes.route("/categories", methods=["POST"])
def CreateCategory():
    """
    Endpoint to create a new category.
    """
    try:
        # Assuming the request body contains JSON data with category details
        data = request.get_json()
        category_name = data.get("category_name")
        if not category_name:
            return jsonify({"error": "Category name is required"}), 400

        # Insert the new category using a DAO method (to be implemented)
        category_id = categories_dao.CreateCategory(category_name)
        if category_id:
            return jsonify({"category_id": category_id}), 201
        else:
            return jsonify({"error": "Failed to create category"}), 500
    except Exception as e:
        print(f"Error creating category: {e}")
        return jsonify({"error": str(e)}), 500


@categories_routes.route("/categories/<int:category_id>", methods=["PUT"])
def UpdateCategory(category_id):
    """
    Endpoint to update an existing category.
    """
    try:
        # Assuming the request body contains JSON data with updated category details
        data = request.get_json()
        description = data.get("description")
        if not description:
            return jsonify({"error": "Description is required"}), 400

        success = categories_dao.UpdateCategory(description, category_id)
        print(f"Success Status: {success}")
        if success:
            return jsonify({"message": "Category updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update category"}), 500
    except Exception as e:
        print(f"Error updating category: {e}")
        return jsonify({"error": str(e)}), 500
