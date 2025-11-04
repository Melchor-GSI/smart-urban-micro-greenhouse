from flask import Blueprint, jsonify

from src.config.database import db

# Create blueprint for main routes
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Main route - homepage"""
    return jsonify(
        {
            "message": "Welcome to the Flask server",
            "status": "success",
        }
    )


@main_bp.route("/api/health")
def health_check():
    if not db.get_database().command("ping"):
        return jsonify(
            {
                "status": "error",
                "message": "Database connection error",
            }
        ), 500
    """Route to check server status"""
    return jsonify({"status": "healthy", "message": "The server is running correctly"})
