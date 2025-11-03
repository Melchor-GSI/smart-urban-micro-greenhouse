from flask import Blueprint, jsonify, request

readings_bp = Blueprint("readings", __name__, url_prefix="/api/readings")

readings_data = [
    {"id": 1, "sensor": "temperature", "value": 22.5, "unit": "C"},
    {"id": 2, "sensor": "humidity", "value": 60, "unit": "%"},
    {"id": 3, "sensor": "pressure", "value": 1013, "unit": "hPa"},
    {"id": 4, "sensor": "luminosity", "value": 300, "unit": "lux"},
]


@readings_bp.route("/", methods=["GET"])
def get_readings():
    return jsonify(
        {"status": "success", "data": readings_data, "count": len(readings_data)}
    )


@readings_bp.route("/", methods=["POST"])
def create_reading():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    required_fields = ["sensor", "value", "unit"]
    for field in required_fields:
        if field not in data:
            return jsonify(
                {"status": "error", "message": f"Required field '{field}' is missing"}
            ), 400

    new_id = max(r["id"] for r in readings_data) + 1 if readings_data else 1

    new_reading = {
        "id": new_id,
        "sensor": data["sensor"],
        "value": data["value"],
        "unit": data["unit"],
    }

    readings_data.append(new_reading)

    return jsonify(
        {
            "status": "success",
            "message": "Reading created successfully",
            "data": new_reading,
        }
    ), 201
