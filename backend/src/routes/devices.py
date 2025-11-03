from flask import Blueprint, jsonify, request

from src.routes.readings import readings_data

devices_bp = Blueprint("devices", __name__, url_prefix="/api/devices")


@devices_bp.route("/<sensor>", methods=["GET"])
def get_reading_by_sensor(sensor):
    devices = [r for r in readings_data if r["sensor"] == sensor]

    if not devices:
        return jsonify({"status": "error", "message": "Variable not found"}), 404

    return jsonify({"status": "success", "data": devices})


@devices_bp.route("/<actuator>/command", methods=["POST"])
def send_command_to_actuator(actuator):
    command_data = request.get_json()

    if not command_data or "command" not in command_data:
        return jsonify({"status": "error", "message": "Command data required"}), 400

    # Here you would implement the actual command sending logic
    # For example, sending to MQTT broker or direct device communication

    return jsonify(
        {
            "status": "success",
            "message": f"Command sent to {actuator}",
            "command": command_data["command"],
        }
    )
