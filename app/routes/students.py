from flask import Blueprint, jsonify, request
from app.dao import StudentDAO

students_routes = Blueprint("students_routes", __name__)
students_dao = StudentDAO()


@students_routes.route("/students", methods=["GET"])
def GetStudents():
    """
    Endpoint to fetch all students.
    """
    try:
        students = students_dao.GetStudents()
        if students is not None:
            return jsonify(students), 200
        else:
            return jsonify(
                {"message": "Could not retrieve students or no students found"}
            ), 404
    except Exception as e:
        print(f"Error fetching students: {e}")
        return jsonify({"error": str(e)}), 500


@students_routes.route("/students/<int:student_id>", methods=["GET"])
def GetStudentById(student_id):
    """
    Endpoint to fetch a student by its ID.
    """
    try:
        student = students_dao.GetStudentById(student_id)
        if student:
            return jsonify(student), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        print(f"Error fetching product by ID: {e}")
        return jsonify({"error": str(e)}), 500


@students_routes.route("/students", methods=["POST"])
def CreateStudent():
    """
    Endpoint to create a new student.
    """
    try:
        data = request.get_json()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        date_of_birth = data.get("date_of_birth")

        if not first_name or not last_name or not email or not date_of_birth:
            return jsonify(
                {"error": "First Name, Last Name, Email and Date of Birth are required"}
            ), 400

        student_id = students_dao.CreateStudent(
            first_name, last_name, email, date_of_birth
        )
        if student_id:
            return jsonify({"student_id": student_id}), 201
        else:
            return jsonify({"error": "Failed to create a Student"}), 500
    except Exception as e:
        print(f"Error creating student: {e}")
        return jsonify({"error": str(e)}), 500


# @students_routes.route('/products/<int:product_id>', methods=['PUT'])
# def UpdateProduct(product_id):
#     try:
#         data = request.get_json()
#         cat_id = data.get("category_id")
#         unit = data.get("unit")
#         price = data.get("price")

#         if not cat_id or not unit or not price:
#             return jsonify({"error": "Category Id, Unit and Price are required"}), 400

#         product = products_dao.UpdateProduct(product_id, cat_id, unit, price)
#         if product:
#             return jsonify(product), 200
#         else:
#             return jsonify({"error": "Product not found"}), 404
#     except Exception as e:
#         print(f"Error updating product: {e}")
#         return jsonify({"error": str(e)}), 500

# @students_routes.route('/products/<int:product_id>', methods=['DELETE'])
# def DeleteProduct(product_id):
#     try:
#         product = products_dao.DeleteProduct(product_id)
#         if product:
#             return jsonify(product), 200
#         else:
#             return jsonify({"error": "Product not found"}), 404
#     except Exception as e:
#         print(f"Error deleting product: {e}")
#         return jsonify({"error": str(e)}), 500
