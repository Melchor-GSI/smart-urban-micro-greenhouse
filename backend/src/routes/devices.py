import logging
from datetime import datetime

from flask import Blueprint, jsonify, request

from src.config.database import db

logger = logging.getLogger(__name__)

devices_bp = Blueprint("devices", __name__, url_prefix="/api/devices")


@devices_bp.route("/", methods=["GET"])
def get_devices():
    try:
        devices_collection = db.get_collection("devices")
        devices = list(devices_collection.find({}, {"_id": 0}))

        return jsonify(
            {"status": "success", "data": devices, "count": len(devices)}
        ), 200

    except Exception as e:
        logger.error(f"Error fetching devices: {e}")
        return jsonify(
            {"status": "error", "message": "Failed to fetch devices", "error": str(e)}
        ), 500


@devices_bp.route("/", methods=["POST"])
def create_device():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        # Add timestamp
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()

        devices_collection = db.get_collection("devices")
        result = devices_collection.insert_one(data)

        return jsonify(
            {
                "status": "success",
                "message": "Device created successfully",
                "device_id": str(result.inserted_id),
            }
        ), 201

    except Exception as e:
        logger.error(f"Error creating device: {e}")
        return jsonify(
            {"status": "error", "message": "Failed to create device", "error": str(e)}
        ), 500


@devices_bp.route("/<device_id>", methods=["GET"])
def get_device(device_id):
    try:
        devices_collection = db.get_collection("devices")
        device = devices_collection.find_one({"device_id": device_id}, {"_id": 0})

        if not device:
            return jsonify({"status": "error", "message": "Device not found"}), 404

        return jsonify({"status": "success", "data": device}), 200

    except Exception as e:
        logger.error(f"Error fetching device {device_id}: {e}")
        return jsonify(
            {"status": "error", "message": "Failed to fetch device", "error": str(e)}
        ), 500
