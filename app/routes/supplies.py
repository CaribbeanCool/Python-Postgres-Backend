from flask import Blueprint, jsonify
from dao.supplies_dao import SuppliesDAO

supplies_routes = Blueprint("supplies_routes", __name__)


# PREFIX IS "/supplies"
@supplies_routes.route("/", methods=["GET"])
def get_all_supplies():
    supplies = SuppliesDAO.GetSupplies()
    return jsonify(supplies)
