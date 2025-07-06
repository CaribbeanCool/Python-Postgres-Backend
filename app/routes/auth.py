from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
import os

auth_routes = Blueprint("auth_routes", __name__)


@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == os.getenv("ADMIN_USERNAME") and password == os.getenv(
        "ADMIN_PASSWORD"
    ):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
