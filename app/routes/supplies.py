from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.supplies_dao import SuppliesDAO

supplies_routes = Blueprint("supplies_routes", __name__)


# PREFIX IS "/supplies"
@supplies_routes.route("/", methods=["GET"])
def get_all_supplies():
    supplies = SuppliesDAO.GetSupplies()
    return jsonify(supplies)
