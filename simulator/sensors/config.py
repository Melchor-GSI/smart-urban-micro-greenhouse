import os

# MQTT broker hostname or IP reachable from the simulator container/process.
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")

# MQTT port (default 1883)
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

# Base publish interval in seconds for each device (can be randomized per-device)
PUBLISH_INTERVAL = float(os.getenv("PUBLISH_INTERVAL", "5.0"))

# Number of simulated devices to run concurrently (1 = single device)
NUM_DEVICES = int(os.getenv("NUM_DEVICES", "1"))

# Prefix for device IDs. Final device IDs will be "{DEVICE_PREFIX}_{i}".
DEVICE_PREFIX = os.getenv("DEVICE_PREFIX", "sensor")

# Topic template. We publish to: sensors/{device_id}/readings
TOPIC_TEMPLATE = os.getenv("TOPIC_TEMPLATE", "sensors/{device_id}/readings")

# Optional jitter to add to interval (seconds) to avoid perfectly synchronized messages.
INTERVAL_JITTER = float(os.getenv("INTERVAL_JITTER", "0.5"))

# MQTT client keepalive
MQTT_KEEPALIVE = int(os.getenv("MQTT_KEEPALIVE", "60"))

# Optional: enable debug logging from the simulator (True/False)
DEBUG = os.getenv("SIMULATOR_DEBUG", "False").lower() in ("1", "true", "yes")

# Sensor types to simulate (each will have NUM_DEVICES instances)
SENSOR_TYPES = ["temperature", "humidity", "air_quality", "soil_moisture"]

"""
Configuration for the sensor simulator.

All configuration values are read from environment variables with fallbacks.
This file keeps settings in one place so the rest of the code is easy to reuse
and test.
"""