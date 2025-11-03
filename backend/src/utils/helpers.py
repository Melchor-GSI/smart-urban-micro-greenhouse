from datetime import datetime


def get_current_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()


def format_response(status, data=None, message=None, error=None):
    """Format standard response for the API"""
    response = {"status": status, "timestamp": get_current_timestamp()}

    if data is not None:
        response["data"] = data

    if message:
        response["message"] = message

    if error:
        response["error"] = error

    return response


def validate_json(data, required_fields):
    """Validate that a JSON has the required fields"""
    if not data:
        return False, "No data received"

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return False, f"Missing the following fields: {', '.join(missing_fields)}"

    return True, None


def safe_get(dictionary, key, default=None):
    """Get value from a dictionary safely"""
    return dictionary.get(key, default)
