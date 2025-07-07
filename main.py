from flask import Flask
from flask_cors import CORS
from app.routes import app_routes
from flask_jwt_extended import JWTManager


app = Flask(__name__)
jwt = JWTManager(app)


CORS(app)

# Register the Blueprint for routes
app.register_blueprint(app_routes, url_prefix="/pg")

if __name__ == "__main__":
    app.run(debug=True)
