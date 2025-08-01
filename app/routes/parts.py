from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.parts_dao import PartsDAO

parts_routes = Blueprint("parts", __name__)


# PREFIX IS "/parts"
@parts_routes.route("/", methods=["GET"])
def get_all_parts():
    parts = PartsDAO.GetParts()
    return jsonify(parts)


@parts_routes.route("/<int:part_id>", methods=["GET"])
def get_part_by_id(part_id):
    part = PartsDAO.GetPartById(part_id)
    if part:
        return jsonify(part)
    return jsonify({"error": "Part not found"}), 404


@parts_routes.route("/", methods=["POST"])
@jwt_required()
def create_part():
    data = request.get_json()
    if not data or "part_name" not in data:
        return jsonify({"error": "Missing part_name"}), 400

    part_id = PartsDAO.CreatePart(data["part_name"])

    if part_id is None:
        return jsonify({"error": "Failed to create part"}), 500

    return jsonify({"message": "Part created successfully", "part_id": part_id}), 201


@parts_routes.route("/<int:part_id>", methods=["PUT"])
@jwt_required()
def update_part(part_id):
    data = request.get_json()
    if not data or "part_name" not in data:
        return jsonify({"error": "Missing part_name"}), 400

    part = PartsDAO.GetPartById(part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    success = PartsDAO.UpdatePart(part_id, data["part_name"])

    if not success:
        return jsonify({"error": "Failed to update part"}), 500

    return jsonify({"message": "Part updated successfully"})


@parts_routes.route("/<int:part_id>", methods=["DELETE"])
@jwt_required()
def delete_part(part_id):
    part = PartsDAO.GetPartById(part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    success = PartsDAO.DeletePart(part_id)

    if not success:
        return jsonify({"error": "Failed to delete part"}), 500

    return jsonify({"message": "Part deleted successfully"})
