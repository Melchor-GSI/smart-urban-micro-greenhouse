import os
import sys

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from src.config.database import db
from src.routes import bp as routes_bp

# Load environment variables
load_dotenv()

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def create_app():
    app = Flask(__name__)

    # Basic configuration
    app.config["DEBUG"] = os.getenv("FLASK_ENV") == "development"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your-secret-key-here")

    # Enable CORS to allow requests from frontend
    CORS(app)

    # Initialize database connection
    try:
        db.connect()
        print("Database connection established successfully")
    except Exception as e:
        print(f"Failed to connect to database: {e}")

    # Register blueprints
    for bp in routes_bp:
        app.register_blueprint(bp)

    # 404 error handler
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "status": "error",
                "message": "Endpoint not found",
                "error": "Not Found",
            }
        ), 404

    # 500 error handler
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify(
            {
                "status": "error",
                "message": "Internal server error",
                "error": "Internal Server Error",
            }
        ), 500

    return app


if __name__ == "__main__":
    # Create the application
    app = create_app()

    # Run the server
    print("🚀 Initializing Flask server...")
    print("📍 Available endpoints:")

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
    )
