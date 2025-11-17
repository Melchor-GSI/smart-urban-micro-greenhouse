from flask_restx import fields


def create_swagger_models(api):
    """Create Swagger models for documentation"""

    # Model for Reading
    reading_model = api.model(
        "Reading",
        {
            "id": fields.String(description="Unique reading ID"),
            "variable": fields.String(
                required=True,
                enum=["temperature", "humidity", "soil_moisture", "co2"],
                description="Type of sensor variable",
            ),
            "sensor": fields.String(required=True, description="Sensor identifier"),
            "value": fields.Float(required=True, description="Reading value"),
            "creation_date": fields.DateTime(description="Creation date"),
        },
    )

    # Model for creating Reading (without id and creation_date)
    reading_create_model = api.model(
        "ReadingCreate",
        {
            "variable": fields.String(
                required=True,
                enum=["temperature", "humidity", "soil_moisture", "co2"],
                description="Type of sensor variable",
            ),
            "sensor": fields.String(required=True, description="Sensor identifier"),
            "value": fields.Float(required=True, description="Reading value"),
        },
    )

    # Model for Event
    event_model = api.model(
        "Event",
        {
            "id": fields.String(description="Unique event ID"),
            "sensor": fields.String(required=True, description="Sensor identifier"),
            "variable": fields.String(
                required=True,
                enum=["temperature", "humidity", "soil_moisture", "co2"],
                description="Variable associated with the event",
            ),
            "event_type": fields.String(
                required=True,
                enum=[
                    "over_limit",
                    "under_limit",
                    "warning_bottom",
                    "warning_top",
                    "disconnected",
                ],
                description="Event type",
            ),
            "urgency": fields.String(
                required=True,
                enum=["low", "medium", "high"],
                description="Urgency level",
            ),
            "status": fields.String(
                required=True,
                enum=["active", "acknowledged", "resolved"],
                description="Event status",
            ),
            "creation_date": fields.DateTime(description="Creation date"),
        },
    )

    # Model for creating Event
    event_create_model = api.model(
        "EventCreate",
        {
            "sensor": fields.String(required=True, description="Sensor identifier"),
            "variable": fields.String(
                required=True,
                enum=["temperature", "humidity", "soil_moisture", "co2"],
                description="Variable associated with the event",
            ),
            "event_type": fields.String(
                required=True,
                enum=[
                    "over_limit",
                    "under_limit",
                    "warning_bottom",
                    "warning_top",
                    "disconnected",
                ],
                description="Event type",
            ),
            "urgency": fields.String(
                required=True,
                enum=["low", "medium", "high"],
                description="Urgency level",
            ),
        },
    )

    # Model for updating Event
    event_update_model = api.model(
        "EventUpdate",
        {
            "id": fields.String(required=True, description="Event ID"),
            "status": fields.String(
                required=True,
                enum=["active", "acknowledged", "resolved"],
                description="New event status",
            ),
        },
    )

    # Model for successful responses
    success_response_model = api.model(
        "SuccessResponse",
        {
            "status": fields.String(example="success"),
            "message": fields.String(description="Success message"),
            "data": fields.Raw(description="Response data"),
            "timestamp": fields.String(description="Response timestamp"),
        },
    )

    # Model for error responses
    error_response_model = api.model(
        "ErrorResponse",
        {
            "status": fields.String(example="error"),
            "message": fields.String(description="Error message"),
            "error": fields.String(description="Error details"),
            "timestamp": fields.String(description="Response timestamp"),
        },
    )

    # Model for current readings
    current_readings_model = api.model(
        "CurrentReadings",
        {
            "timestamp": fields.DateTime(description="Response timestamp"),
            "temperature": fields.Float(description="Current temperature"),
            "humidity": fields.Float(description="Current humidity"),
            "soil_moisture": fields.Float(description="Current soil moisture"),
            "co2": fields.Float(description="Current CO2 level"),
        },
    )

    return {
        "reading": reading_model,
        "reading_create": reading_create_model,
        "event": event_model,
        "event_create": event_create_model,
        "event_update": event_update_model,
        "success_response": success_response_model,
        "error_response": error_response_model,
        "current_readings": current_readings_model,
    }
