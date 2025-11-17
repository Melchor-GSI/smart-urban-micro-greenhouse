from flask_restx import Api

# Swagger/OpenAPI Configuration
api_config = {
    "title": "Smart Urban Micro-Greenhouse API",
    "version": "1.0",
    "description": "API for the IoT system with sensor readings and event management",
    "doc": "/",  # Documentation available at the root
    "prefix": "/api",
}


def init_swagger(app):
    """Initialize Swagger with Flask-RESTX"""
    api = Api(app, **api_config)
    return api
