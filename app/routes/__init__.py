from flask import Blueprint
from routes.categories import categories_routes
from routes.customers import customers_routes
from routes.orders import orders_routes
from routes.products import products_routes
from routes.students import students_routes
from routes.auth import auth_routes

app_routes = Blueprint("app_routes", __name__)

# Register individual table blueprints
app_routes.register_blueprint(categories_routes)
app_routes.register_blueprint(customers_routes)
app_routes.register_blueprint(orders_routes)
app_routes.register_blueprint(products_routes)
app_routes.register_blueprint(students_routes)

app_routes.register_blueprint(auth_routes)
