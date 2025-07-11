from flask import Flask
from flask_cors import CORS
from routes import app_routes
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("ADMIN_USERNAME")
jwt = JWTManager(app)

CORS(app)

# Register the Blueprint for routes
app.register_blueprint(app_routes, url_prefix="/pg")

if __name__ == "__main__":
    app.run(debug=True)
