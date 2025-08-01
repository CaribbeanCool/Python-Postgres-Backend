from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.supplier_dao import SupplierDAO

supplier_routes = Blueprint("supplier", __name__)


# PREFIX IS "/suppliers"
@supplier_routes.route("/", methods=["GET"])
def get_all_suppliers():
    suppliers = SupplierDAO.GetSuppliers()
    return jsonify(suppliers)


@supplier_routes.route("/<int:supplier_id>", methods=["GET"])
def get_supplier_by_id(supplier_id):
    supplier = SupplierDAO.GetSupplierById(supplier_id)
    if supplier:
        return jsonify(supplier)
    else:
        return jsonify({"error": "Supplier not found"}), 404


@supplier_routes.route("/", methods=["POST"])
@jwt_required()
def create_supplier():
    data = request.get_json()

    if not data or "supplier_name" not in data:
        return jsonify({"error": "Missing supplier_name parameter"}), 400

    supplier_name = data["supplier_name"]
    supplier_id = SupplierDAO.CreateSupplier(supplier_name)

    if supplier_id is None:
        return jsonify({"error": "Failed to create supplier"}), 500

    return jsonify(
        {"message": "Supplier created successfully", "supplier_id": supplier_id}
    ), 201


@supplier_routes.route("/<int:supplier_id>", methods=["PUT"])
@jwt_required()
def update_supplier(supplier_id):
    data = request.get_json()

    if not data or "supplier_name" not in data:
        return jsonify({"error": "Missing supplier_name parameter"}), 400

    supplier_name = data["supplier_name"]
    supplier = SupplierDAO.GetSupplierById(supplier_id)

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    success = SupplierDAO.UpdateSupplier(supplier_id, supplier_name)

    if not success:
        return jsonify({"error": "Failed to update supplier"}), 500

    return jsonify({"message": "Supplier updated successfully"})


@supplier_routes.route("/<int:supplier_id>", methods=["DELETE"])
@jwt_required()
def delete_supplier(supplier_id):
    supplier = SupplierDAO.GetSupplierById(supplier_id)

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    success = SupplierDAO.DeleteSupplier(supplier_id)

    if not success:
        return jsonify({"error": "Failed to delete supplier"}), 500

    return jsonify({"message": "Supplier deleted successfully"})
