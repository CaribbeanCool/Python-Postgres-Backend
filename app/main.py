from flask import Flask
from flask_cors import CORS
from routes import app_routes
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from server import GetDBConnection
from datetime import timedelta
import os

load_dotenv()


def CheckDatabaseConnection():
    """
    Check if database is available on startup
    """
    print("Checking database connection...")
    try:
        conn = GetDBConnection()
        if conn is None:
            print("❌ ERROR: Database connection failed!")
            print("   Make sure your PostgreSQL Docker container is running")
            print("   Command: docker-compose up -d")
            return False
        else:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    print("✅ Database connection successful!")
                    conn.close()
                    return True
    except Exception as e:
        print(f"❌ ERROR: Database connection failed - {e}")
        print("   Make sure your PostgreSQL Docker container is running")
        print("   Command: docker start my-postgres")
        return False
    return False


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("ADMIN_USERNAME")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)  # Example: 30 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)  # Example: 7 days
jwt = JWTManager(app)

CORS(app)

if not CheckDatabaseConnection():
    print("\n⚠️  WARNING: Starting server without database connection")
    print("   The endpoints may not work properly")
    print("   Please start your database and restart the server\n")
else:
    print("🚀 Server ready with database connection\n")

# Register the Blueprint for routes
app.register_blueprint(app_routes, url_prefix="/pg")

if __name__ == "__main__":
    app.run(debug=True)
