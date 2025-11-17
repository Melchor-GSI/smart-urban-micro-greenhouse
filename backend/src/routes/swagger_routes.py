import logging
import uuid
from datetime import datetime, timedelta

from flask import request
from flask_restx import Namespace, Resource

from src.config.database import db
from src.models.event import Event
from src.models.reading import VARIABLE_TYPES, Reading, ReadingsResponse
from src.models.swagger_models import create_swagger_models
from src.services.events import EventService
from src.services.readings import ReadingService
from src.utils.helpers import format_response

logger = logging.getLogger(__name__)


def register_swagger_routes(api):
    """Register all routes with Swagger documentation"""

    # Create Swagger models
    models = create_swagger_models(api)

    # Create namespaces
    readings_ns = Namespace(
        "readings", description="Operations related to sensor readings"
    )
    events_ns = Namespace("events", description="Operations related to system events")
    health_ns = Namespace("health", description="System health endpoints")

    # === READINGS NAMESPACE ===

    @readings_ns.route("/")
    class ReadingsResource(Resource):
        @readings_ns.doc("get_readings")
        @readings_ns.marshal_list_with(models["success_response"])
        def get(self):
            """Get all sensor readings"""
            try:
                reading_service = ReadingService()
                readings = reading_service.get_items()
                data = [r.model_dump() for r in readings]
                data.reverse()

                return format_response(
                    status="success",
                    data=data,
                    message=f"Found {len(readings)} readings",
                ), 200

            except Exception as e:
                logger.error(f"Error fetching readings: {e}")
                return format_response(
                    status="error", message="Failed to fetch readings", error=str(e)
                ), 500

        @readings_ns.doc("create_reading")
        @readings_ns.expect(models["reading_create"])
        @readings_ns.marshal_with(models["success_response"])
        def post(self):
            """Create a new sensor reading"""
            try:
                data = request.get_json()

                if not data:
                    return format_response(
                        status="error", message="No data provided"
                    ), 400

                try:
                    new_reading = Reading(
                        id=str(uuid.uuid4()),
                        variable=data["variable"],
                        sensor=data["sensor"],
                        value=data["value"],
                    )
                except Exception as ve:
                    return format_response(
                        status="error", message="Invalid reading data", error=str(ve)
                    ), 400

                readings_collection = db.get_collection("readings")
                readings_collection.insert_one(new_reading.model_dump())

                return format_response(
                    status="success",
                    message="Reading created successfully",
                    data=new_reading.model_dump(),
                ), 201

            except Exception as e:
                logger.error(f"Error creating reading: {e}")
                return format_response(
                    status="error", message="Failed to create reading", error=str(e)
                ), 500

    @readings_ns.route("/now/")
    class CurrentReadingsResource(Resource):
        @readings_ns.doc("get_current_readings")
        @readings_ns.marshal_with(models["success_response"])
        def get(self):
            """Get current readings from all sensors"""
            try:
                reading_service = ReadingService()
                current_readings = reading_service.get_items(now=True)

                if not current_readings:
                    return format_response(
                        status="error", message="No current readings found"
                    ), 404

                response_dict = {}
                for variable in VARIABLE_TYPES.__args__:
                    response_dict[variable] = next(
                        (r.value for r in current_readings if r.variable == variable),
                        None,
                    )

                response = ReadingsResponse(**response_dict)

                return format_response(
                    status="success", data=response.model_dump()
                ), 200

            except Exception as e:
                logger.error(f"Error fetching current readings: {e}")
                return format_response(
                    status="error",
                    message="Failed to fetch current readings",
                    error=str(e),
                ), 500

    @readings_ns.route("/<string:variable>/last-hours")
    class ReadingsLastHoursResource(Resource):
        @readings_ns.doc("get_readings_last_hours")
        @readings_ns.param(
            "variable", "Sensor variable (temperature, humidity, soil_moisture, co2)"
        )
        @readings_ns.param(
            "hours", "Number of hours back (default: 6, maximum: 168)", type=int
        )
        @readings_ns.marshal_with(models["success_response"])
        def get(self, variable):
            """Get readings for a specific variable from the last N hours"""
            hours = request.args.get("hours", 6, type=int)

            try:
                if hours <= 0 or hours > 168:
                    return format_response(
                        status="error",
                        message="Hours parameter must be between 1 and 168 (7 days)",
                    ), 400

                reading_service = ReadingService()
                readings = reading_service.get_items(
                    variable=variable, hours_back=hours
                )

                time_threshold = datetime.utcnow() - timedelta(hours=hours)

                return format_response(
                    status="success",
                    data={
                        "readings": [r.model_dump() for r in readings],
                        "count": len(readings),
                        "variable": variable,
                        "hours_back": hours,
                        "from_time": time_threshold.isoformat(),
                        "to_time": datetime.utcnow().isoformat(),
                    },
                ), 200

            except Exception as e:
                logger.error(f"Error fetching readings for variable {variable}: {e}")
                return format_response(
                    status="error",
                    message=f"Failed to fetch readings for variable '{variable}'",
                    error=str(e),
                ), 500

    # === EVENTS NAMESPACE ===

    @events_ns.route("/")
    class EventsResource(Resource):
        @events_ns.doc("get_events")
        @events_ns.param("status", "Filter by status (active, acknowledged, resolved)")
        @events_ns.marshal_with(models["success_response"])
        def get(self):
            """Get all events with optional status filtering"""
            try:
                event_service = EventService()
                status = request.args.get("status")
                events = event_service.get_items(status=status)

                return format_response(
                    status="success",
                    data=[event.model_dump() for event in events],
                    message=f"Found {len(events)} events",
                ), 200

            except Exception as e:
                return format_response(
                    status="error", message="Failed to fetch events", error=str(e)
                ), 500

        @events_ns.doc("create_event")
        @events_ns.expect(models["event_create"])
        @events_ns.marshal_with(models["success_response"])
        def post(self):
            """Create a new event"""
            try:
                event_service = EventService()
                data = request.get_json()

                if not data:
                    return format_response(
                        status="error", message="No data provided"
                    ), 400

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
                    return format_response(
                        status="error", message=f"Missing required field: {str(e)}"
                    ), 400

                if event_service.active_event(new_event):
                    return format_response(
                        status="success",
                        message="An active or acknowledged event with the same variable and event_type already exists",
                    ), 200

                success = event_service.set_item(new_event)

                if not success:
                    return format_response(
                        status="error", message="Failed to create event in database"
                    ), 500

                return format_response(
                    status="success",
                    message="Event created successfully",
                    data=new_event.model_dump(),
                ), 201

            except Exception as e:
                return format_response(
                    status="error", message="Failed to create event", error=str(e)
                ), 500

        @events_ns.doc("update_event")
        @events_ns.expect(models["event_update"])
        @events_ns.marshal_with(models["success_response"])
        def patch(self):
            """Update the status of an existing event"""
            try:
                event_service = EventService()
                data = request.get_json()

                if not data:
                    return format_response(
                        status="error", message="No data provided"
                    ), 400

                try:
                    event_id = data["id"]
                    new_status = data["status"]
                except KeyError as e:
                    return format_response(
                        status="error", message=f"Missing required field: {str(e)}"
                    ), 400

                success = event_service.patch_item(event_id, {"status": new_status})

                if not success:
                    return format_response(
                        status="error", message="Event not found"
                    ), 404

                return format_response(
                    status="success", message="Event updated successfully"
                ), 200

            except Exception as e:
                return format_response(
                    status="error", message="Failed to update event", error=str(e)
                ), 500

    # === HEALTH NAMESPACE ===

    @health_ns.route("/")
    class HealthResource(Resource):
        @health_ns.doc("health_check")
        def get(self):
            """Check system health status"""
            try:
                if not db.get_database().command("ping"):
                    return format_response(
                        status="error", message="Database connection error"
                    ), 500

                return format_response(
                    status="healthy", message="The server is running correctly"
                ), 200

            except Exception as e:
                return format_response(
                    status="error", message="Health check failed", error=str(e)
                ), 500

    # Register namespaces in the API
    api.add_namespace(readings_ns, path="/api/readings")
    api.add_namespace(events_ns, path="/api/events")
    api.add_namespace(health_ns, path="/api/health")
