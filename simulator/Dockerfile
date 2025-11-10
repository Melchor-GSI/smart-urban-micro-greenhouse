# Use Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /simulator

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the simulator code
COPY . .

# Set environment variables (you can override in docker-compose)
ENV MQTT_BROKER=mqtt-broker
ENV MQTT_PORT=1883
ENV PUBLISH_INTERVAL=5.0
ENV NUM_DEVICES=1
ENV DEVICE_PREFIX=sensor

# Run the simulator
CMD ["python", "-m", "sensors.run_simulator"]