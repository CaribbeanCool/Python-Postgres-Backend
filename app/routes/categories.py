from flask import Blueprint, jsonify, request
from dao import CategoriesDAO

categories_routes = Blueprint("categories_routes", __name__)
# Remove this line - no need to instantiate with static methods
# categories_dao = CategoriesDAO()


@categories_routes.route("/categories", methods=["GET"])
def GetCategories():
    """
    Endpoint to fetch all categories.
    """
    try:
        categories = CategoriesDAO.GetCategories()
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
        category = CategoriesDAO.GetCategoryByID(
            category_id
        )  # Call static method directly
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
        data = request.get_json()
        category_name = data.get("category_name")
        description = data.get("description", "")

        if not category_name:
            return jsonify({"error": "Category name is required"}), 400

        success = CategoriesDAO.CreateCategory(category_name, description)
        if success:
            return jsonify({"message": "Category created successfully"}), 201
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
        data = request.get_json()
        category_name = data.get("category_name")
        description = data.get("description")

        if not category_name or not description:
            return jsonify({"error": "Category name and description are required"}), 400

        success = CategoriesDAO.UpdateCategory(category_id, category_name, description)
        print(f"Success Status: {success}")
        if success:
            return jsonify({"message": "Category updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update category"}), 500
    except Exception as e:
        print(f"Error updating category: {e}")
        return jsonify({"error": str(e)}), 500
