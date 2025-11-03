from flask import Blueprint, jsonify, request

events_bp = Blueprint("events", __name__, url_prefix="/api/events")

events_data = [
    {"id": 1, "name": "Event 1", "description": "Description of event 1"},
    {"id": 2, "name": "Event 2", "description": "Description of event 2"},
    {"id": 3, "name": "Event 3", "description": "Description of event 3"},
]


@events_bp.route("/", methods=["GET"])
def get_events():
    return jsonify(
        {"status": "success", "data": events_data, "count": len(events_data)}
    )


@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    """Get a specific event by ID"""
    event = next((e for e in events_data if e["id"] == event_id), None)

    if event:
        return jsonify({"status": "success", "data": event})
    else:
        return jsonify(
            {"status": "error", "message": f"Event with ID {event_id} not found"}
        ), 404


@events_bp.route("/", methods=["POST"])
def create_event():
    """Create a new event"""
    data = request.get_json()

    if not data or "name" not in data or "description" not in data:
        return jsonify(
            {
                "status": "error",
                "message": "Required fields: name and description",
            }
        ), 400

    new_id = max([e["id"] for e in events_data]) + 1 if events_data else 1
    new_event = {"id": new_id, "name": data["name"], "description": data["description"]}

    events_data.append(new_event)

    return jsonify(
        {
            "status": "success",
            "message": "Event created successfully",
            "data": new_event,
        }
    ), 201
