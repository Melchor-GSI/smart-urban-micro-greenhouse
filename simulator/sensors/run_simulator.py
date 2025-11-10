import threading
import time
import logging
import signal
import sys
from typing import List
import random

from .config import (
    NUM_DEVICES,
    DEVICE_PREFIX,
    PUBLISH_INTERVAL,
    INTERVAL_JITTER,
    TOPIC_TEMPLATE,
    DEBUG,
    SENSOR_TYPES,
)
from .mqtt_client import MQTTClient
from .sensor import SensorSimulator

logger = logging.getLogger("simulator.run")
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# Graceful shutdown handling
_stop_event = threading.Event()


def _signal_handler(signum, frame):
    logger.info("Received signal %s, stopping simulator...", signum)
    _stop_event.set()


signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)


def device_loop(device_id: str, sensor_type: str, publish_interval: float):
    """
    Each device runs this loop:
      - connect to broker (the MQTTClient handles reconnect in background)
      - generate reading, publish to topic
      - sleep for interval +/- jitter
    """
    client = MQTTClient(client_id=f"{device_id}_client")
    client.connect()
    sim = SensorSimulator(device_id=device_id, sensor_type=sensor_type)

    try:
        while not _stop_event.is_set():
            payload = sim.generate_reading()
            topic = TOPIC_TEMPLATE.format(device_id=device_id)
            client.publish(topic, payload)
            logger.info("Published device=%s topic=%s", device_id, topic)

            # Add jitter to avoid synchronized publishes
            sleep_time = publish_interval + (INTERVAL_JITTER * (0.5 - random.random()))
            # ensure non-negative
            sleep_time = max(0.1, sleep_time)
            # wait in small increments so we can exit faster on signal
            waited = 0.0
            while waited < sleep_time and not _stop_event.is_set():
                time.sleep(0.2)
                waited += 0.2
    except Exception:
        logger.exception("Exception in device loop for %s", device_id)
    finally:
        client.stop()
        logger.info("Device %s stopped", device_id)


def start_simulators(num_devices: int, device_prefix: str, base_interval: float) -> List[threading.Thread]:
    """
    Create threads and start simulated devices. Returns list of thread objects.
    """
    threads: List[threading.Thread] = []

    for sensor_type in SENSOR_TYPES:
        for i in range(1, num_devices + 1):
            device_id = f"{sensor_type}_{i:02d}"
            # small per-device variation to interval so devices don't publish exactly at same time
            per_device_interval = base_interval * (1.0 + (0.1 * ((i % 3) - 1)))
            t = threading.Thread(
                target=device_loop,
                args=(device_id, sensor_type, per_device_interval),
                daemon=True,
            )
            t.start()
            threads.append(t)
            logger.info("Started %s (%s, interval %.2fs)", device_id, sensor_type, per_device_interval)
            # small stagger when starting threads
            time.sleep(0.1)

    return threads


def main():
    logger.info("Starting sensor simulator with %d devices per type", NUM_DEVICES)
    threads = start_simulators(NUM_DEVICES, DEVICE_PREFIX, PUBLISH_INTERVAL)

    # Wait until stop event is set
    try:
        while not _stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, exiting...")

    # join threads briefly
    logger.info("Waiting for threads to finish...")
    for t in threads:
        t.join(timeout=1.0)
    logger.info("Simulator stopped.")


if __name__ == "__main__":
    main()

"""
Run the sensor simulator.

- Reads configuration from simulators/sensors/config.py
- Starts `NUM_DEVICES` simulated devices (each in its own thread)
- Each device creates an MQTTClient and SensorSimulator and publishes to TOPIC_TEMPLATE

Run as module:
    python -m sensors.run_simulator

You can also run the module inside Docker as the container CMD.
"""