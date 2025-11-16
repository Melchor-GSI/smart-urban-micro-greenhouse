import uuid

from flask import Blueprint, jsonify, request

from src.models.event import Event
from src.services.events import EventService

events_bp = Blueprint("events", __name__, url_prefix="/api/events")


@events_bp.route("/", methods=["GET"])
def get_events():
    try:
        event_service = EventService()

        # Get status parameter from query string
        status = request.args.get("status")

        # Get events with optional status filtering
        events = event_service.get_items(status=status)

        return jsonify(
            {
                "status": "success",
                "data": [event.model_dump() for event in events],
                "count": len(events),
            }
        ), 200

    except Exception as e:
        return jsonify(
            {"status": "error", "message": "Failed to fetch events", "error": str(e)}
        ), 500


@events_bp.route("/", methods=["POST"])
def create_event():
    """Create a new event"""
    try:
        event_service = EventService()
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        # Create Event object for validation
        try:
            new_event = Event(
                id=str(uuid.uuid4()),
                sensor=data["sensor"],
                variable=data["variable"],
                event_type=data["event_type"],
                urgency=data["urgency"],
                status="active",
            )
        except KeyError as e:
            return jsonify(
                {"status": "error", "message": f"Missing required field: {str(e)}"}
            ), 400
        except Exception as e:
            return jsonify(
                {"status": "error", "message": "Invalid event data", "error": str(e)}
            ), 400

        if event_service.active_event(new_event):
            return jsonify(
                {
                    "status": "success",
                    "message": "An active or acknowledged event with the same variable and event_type already exists",
                }
            ), 200

        # Insert into database
        success = event_service.set_item(new_event)
        # TODO: send notification to frontend
        if not success:
            return jsonify(
                {"status": "error", "message": "Failed to create event in database"}
            ), 500

        return jsonify(
            {
                "status": "success",
                "message": "Event created successfully",
                "data": new_event.model_dump(),
            }
        ), 201

    except Exception as e:
        return jsonify(
            {"status": "error", "message": "Failed to create event", "error": str(e)}
        ), 500


@events_bp.route("/", methods=["PATCH"])
def update_event():
    """Update an existing event's status"""
    try:
        event_service = EventService()
        data = request.get_json()

        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        try:
            event_id = data["id"]
            new_status = data["status"]
        except KeyError as e:
            return jsonify(
                {"status": "error", "message": f"Missing required field: {str(e)}"}
            ), 400

        # Update event in the database
        success = event_service.patch_item(event_id, {"status": new_status})

        if not success:
            return jsonify({"status": "error", "message": "Event not found"}), 404

        return jsonify(
            {"status": "success", "message": "Event updated successfully"}
        ), 200

    except Exception as e:
        return jsonify(
            {"status": "error", "message": "Failed to update event", "error": str(e)}
        ), 500
