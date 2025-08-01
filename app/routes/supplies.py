from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.supplies_dao import SuppliesDAO

supplies_routes = Blueprint("supplies", __name__)


# PREFIX IS "/supplies"
@supplies_routes.route("/", methods=["GET"])
def get_all_supplies():
    supplies = SuppliesDAO.GetSupplies()
    return jsonify(supplies)


@supplies_routes.route("/<int:supply_id>", methods=["GET"])
def get_supply_by_id(supply_id):
    supply = SuppliesDAO.GetSupplyById(supply_id)
    if supply:
        return jsonify(supply)
    return jsonify({"error": "Supply not found"}), 404


@supplies_routes.route("/", methods=["POST"])
@jwt_required()
def create_supply():
    data = request.get_json()
    if (
        not data
        or "supplier_id" not in data
        or "part_id" not in data
        or "quantity" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    supply_id = SuppliesDAO.CreateSupply(
        data["supplier_id"], data["part_id"], data["quantity"]
    )

    if supply_id is None:
        return jsonify({"error": "Failed to create supply"}), 500

    return jsonify(
        {"message": "Supply created successfully", "supply_id": supply_id}
    ), 201


@supplies_routes.route("/<int:supply_id>", methods=["PUT"])
@jwt_required()
def update_supply(supply_id):
    data = request.get_json()
    if not data or "quantity" not in data:
        return jsonify({"error": "Missing quantity"}), 400

    supply = SuppliesDAO.GetSupplyById(supply_id)
    if not supply:
        return jsonify({"error": "Supply not found"}), 404

    success = SuppliesDAO.UpdateSupply(supply_id, data["quantity"])

    if not success:
        return jsonify({"error": "Failed to update supply"}), 500

    return jsonify({"message": "Supply updated successfully"})


@supplies_routes.route("/<int:supply_id>", methods=["DELETE"])
@jwt_required()
def delete_supply(supply_id):
    supply = SuppliesDAO.GetSupplyById(supply_id)
    if not supply:
        return jsonify({"error": "Supply not found"}), 404

    success = SuppliesDAO.DeleteSupply(supply_id)

    if not success:
        return jsonify({"error": "Failed to delete supply"}), 500

    return jsonify({"message": "Supply deleted successfully"})
