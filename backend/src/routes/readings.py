import logging
import uuid

from flask import Blueprint, jsonify, request

from src.config.database import db
from src.models.reading import Reading
from src.services.readings import ReadingService

logger = logging.getLogger(__name__)

readings_bp = Blueprint("readings", __name__, url_prefix="/api/readings")


@readings_bp.route("/", methods=["GET"])
def get_readings():
    try:
        reading_service = ReadingService()

        readings = reading_service.get_items()

        return jsonify(
            {
                "status": "success",
                "data": [r.model_dump() for r in readings],
                "count": len(readings),
            }
        ), 200

    except Exception as e:
        logger.error(f"Error fetching readings: {e}")
        return jsonify(
            {"status": "error", "message": "Failed to fetch readings", "error": str(e)}
        ), 500


@readings_bp.route("/", methods=["POST"])
def create_reading():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        try:
            # Add timestamp
            new_reading = Reading(
                id=str(uuid.uuid4()),
                variable=data["variable"],
                sensor=data["sensor"],
                value=data["value"],
            )
        except Exception as ve:
            return jsonify(
                {
                    "status": "error",
                    "message": "Invalid reading data",
                    "error": str(ve),
                }
            ), 400

        readings_collection = db.get_collection("readings")
        readings_collection.insert_one(new_reading.model_dump())

        return jsonify(
            {
                "status": "success",
                "message": "Reading created successfully",
            }
        ), 201

    except Exception as e:
        logger.error(f"Error creating reading: {e}")
        return jsonify(
            {"status": "error", "message": "Failed to create reading", "error": str(e)}
        ), 500


@readings_bp.route("/<sensor>", methods=["GET"])
def get_readings_by_sensor(sensor):
    try:
        readings_collection = db.get_collection("readings")

        # Get query parameters
        limit = request.args.get("limit", 100, type=int)

        readings = list(
            readings_collection.find({"sensor": sensor}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )

        if not readings:
            return jsonify(
                {"status": "error", "message": "No readings found for this sensor"}
            ), 404

        return jsonify(
            {"status": "success", "data": readings, "count": len(readings)}
        ), 200

    except Exception as e:
        logger.error(f"Error fetching readings for sensor {sensor}: {e}")
        return jsonify(
            {"status": "error", "message": "Failed to fetch readings", "error": str(e)}
        ), 500
