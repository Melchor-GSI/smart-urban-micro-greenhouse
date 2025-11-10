import time
import queue
import threading
import logging
import paho.mqtt.client as mqtt
from .config import MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE, DEBUG

logger = logging.getLogger("simulator.mqtt")
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


class MQTTClient:
    """
    Minimal MQTT client with reconnect loop and an outbound queue.

    Usage:
        client = MQTTClient(client_id="sim_1")
        client.connect()
        client.publish(topic, payload)
    """

    def __init__(self, client_id="sensor_simulator"):
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self._connected = False
        self._out_queue = queue.Queue()
        self._loop_thread = None
        self._stop_event = threading.Event()

    def _on_connect(self, client, userdata, flags, rc):
        """MQTT on_connect callback."""
        if rc == 0:
            logger.info("[MQTT] Connected to broker.")
            self._connected = True
            # flush outbound queue
            while not self._out_queue.empty():
                topic, payload = self._out_queue.get_nowait()
                logger.debug("[MQTT] Flushing queued message to %s", topic)
                self.client.publish(topic, payload)
        else:
            logger.warning("[MQTT] Bad connection. RC=%s", rc)

    def _on_disconnect(self, client, userdata, rc):
        """MQTT on_disconnect callback."""
        logger.warning("[MQTT] Disconnected from broker (rc=%s). Will attempt reconnect.", rc)
        self._connected = False

    def connect(self):
        """Start connect + background loop with automatic retry."""
        self._stop_event.clear()

        def _run_loop():
            while not self._stop_event.is_set():
                try:
                    if not self._connected:
                        logger.info("[MQTT] Trying to connect to %s:%s", MQTT_BROKER, MQTT_PORT)
                        self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=MQTT_KEEPALIVE)
                        self.client.loop_start()
                    # sleep a bit and re-check connection status
                    time.sleep(2)
                except Exception as e:
                    logger.exception("[MQTT] Connection attempt failed: %s", e)
                    time.sleep(3)

        self._loop_thread = threading.Thread(target=_run_loop, daemon=True)
        self._loop_thread.start()

    def stop(self):
        """Stop the client and network loop."""
        self._stop_event.set()
        try:
            self.client.loop_stop()
            self.client.disconnect()
        except Exception:
            pass
        logger.info("[MQTT] Client stopped.")

    def publish(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        """
        Publish a message. If not connected, store in an outbound queue to publish
        once connected.
        """
        if self._connected:
            logger.debug("[MQTT] Publishing to %s: %s", topic, payload)
            self.client.publish(topic, payload, qos=qos, retain=retain)
        else:
            logger.debug("[MQTT] Not connected. Queueing message for %s", topic)
            self._out_queue.put((topic, payload))

"""
MQTT client helper for the sensor simulator.

This module provides a small MQTTClient class that:
 - connects to a broker (with retries),
 - starts the network loop in a background thread,
 - exposes a publish() method that queues messages when not connected.

The wrapper keeps run_simulator.py concise and focuses on publishing logic.
"""