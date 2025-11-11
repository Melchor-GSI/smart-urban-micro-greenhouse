import logging
import uuid
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from src.config.database import db
from src.models.reading import (
    VARIABLE_TYPES,
    Reading,
    ReadingsResponse,
)
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


@readings_bp.route("/now", methods=["GET"])
def get_current_readings():
    try:
        reading_service = ReadingService()

        current_readings = reading_service.get_items(now=True)

        if not current_readings:
            return jsonify(
                {"status": "error", "message": "No current readings found"}
            ), 404

        response_dict = {}
        for variable in VARIABLE_TYPES.__args__:
            response_dict[variable] = next(
                (r.value for r in current_readings if r.variable == variable), None
            )

        response = ReadingsResponse(**response_dict)

        return jsonify(
            {
                "status": "success",
                "data": response.model_dump(),
            }
        ), 200

    except Exception as e:
        logger.error(f"Error fetching current readings: {e}")
        return jsonify(
            {
                "status": "error",
                "message": "Failed to fetch current readings",
                "error": str(e),
            }
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


@readings_bp.route("/<variable>/last-hours", methods=["GET"])
def get_readings_last_hours(variable):
    """
    Get readings for a specific variable from the last N hours (configurable via query parameter)
    """
    # Get hours parameter from query string, default to 6 hours
    hours = request.args.get("hours", 6, type=int)
    try:
        # Validate hours parameter
        if hours <= 0 or hours > 168:  # Max 7 days (168 hours)
            return jsonify(
                {
                    "status": "error",
                    "message": "Hours parameter must be between 1 and 168 (7 days)",
                }
            ), 400

        reading_service = ReadingService()
        readings = reading_service.get_items(variable=variable, hours_back=hours)

        # Calculate time range for response
        time_threshold = datetime.utcnow() - timedelta(hours=hours)

        return jsonify(
            {
                "status": "success",
                "data": [r.model_dump() for r in readings],
                "count": len(readings),
                "variable": variable,
                "hours_back": hours,
                "from_time": time_threshold.isoformat(),
                "to_time": datetime.utcnow().isoformat(),
            }
        ), 200

    except Exception as e:
        logger.error(
            f"Error fetching readings for variable {variable} in last {hours} hours: {e}"
        )
        return jsonify(
            {
                "status": "error",
                "message": f"Failed to fetch readings for variable '{variable}'",
                "error": str(e),
            }
        ), 500
