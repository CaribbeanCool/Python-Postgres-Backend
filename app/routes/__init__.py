from flask import Blueprint
from routes.categories import categories_routes
from routes.customers import customers_routes
from routes.orders import orders_routes
from routes.products import products_routes
from routes.students import students_routes
from routes.auth import auth_routes
from routes.supplier import supplier_routes
from routes.parts import parts_routes
from routes.supplies import supplies_routes

app_routes = Blueprint("app_routes", __name__)

# Register individual table blueprints
app_routes.register_blueprint(categories_routes)
app_routes.register_blueprint(customers_routes)
app_routes.register_blueprint(orders_routes)
app_routes.register_blueprint(products_routes)
app_routes.register_blueprint(students_routes)

# Register supply chain blueprints
app_routes.register_blueprint(supplier_routes, url_prefix="/suppliers")
app_routes.register_blueprint(parts_routes, url_prefix="/parts")
app_routes.register_blueprint(supplies_routes, url_prefix="/supplies")

app_routes.register_blueprint(auth_routes)
