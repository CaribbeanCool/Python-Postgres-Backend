from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from dao import StudentDAO

students_routes = Blueprint("students_routes", __name__)


@students_routes.route("/students", methods=["GET"])
@jwt_required()
def GetStudents():
    """
    Endpoint to fetch all students.
    """
    try:
        students = StudentDAO.GetStudents()
        if students is not None:
            return jsonify(students), 200
        else:
            return jsonify({"error": "Failed to fetch students"}), 500
    except Exception as e:
        print(f"Error fetching students: {e}")
        return jsonify({"error": str(e)}), 500


@students_routes.route("/students/<int:student_id>", methods=["GET"])
def GetStudentById(student_id):
    """
    Endpoint to fetch a student by its ID.
    """
    try:
        student = StudentDAO.GetStudentById(student_id)
        if student:
            return jsonify(student), 200
        else:
            return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        print(f"Error fetching student by ID: {e}")
        return jsonify({"error": str(e)}), 500


@students_routes.route("/students", methods=["POST"])
@jwt_required()
def CreateStudent():
    """
    Endpoint to create a new student.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        date_of_birth = data.get("date_of_birth")

        if not first_name or not last_name or not email or not date_of_birth:
            return jsonify(
                {"error": "First Name, Last Name, Email and Date of Birth are required"}
            ), 400

        student_id = StudentDAO.CreateStudent(
            first_name, last_name, email, date_of_birth
        )
        if student_id:
            return jsonify(
                {"student_id": student_id, "message": "Student created successfully"}
            ), 201
        else:
            return jsonify({"error": "Failed to create student"}), 500
    except Exception as e:
        print(f"Error creating student: {e}")
        return jsonify({"error": str(e)}), 500
