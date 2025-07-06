from flask import Blueprint
from app.routes.categories import categories_routes
from app.routes.customers import customers_routes
from app.routes.orders import orders_routes
from app.routes.products import products_routes
from app.routes.students import students_routes

app_routes = Blueprint("app_routes", __name__)

# Register individual table blueprints
app_routes.register_blueprint(categories_routes)
app_routes.register_blueprint(customers_routes)
app_routes.register_blueprint(orders_routes)
app_routes.register_blueprint(products_routes)
app_routes.register_blueprint(students_routes)
