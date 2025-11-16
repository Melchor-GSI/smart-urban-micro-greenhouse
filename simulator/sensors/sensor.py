import math
import random
import json
from datetime import datetime, timezone
from typing import Dict

# Seed the RNG for repeatable demos if desired (comment out for more randomness)
# random.seed(42)

class SensorSimulator:
    """
    Per-device sensor simulator.
    Call `generate_reading()` to get a JSON string representing the latest reading.

    The object stores internal state so values evolve smoothly over time.
    """

    def __init__(self, device_id: str, sensor_type: str):
        self.device_id = device_id
        self.sensor_type = sensor_type
        self._reading_count = 0
        self._initialize_state()

    def _initialize_state(self):
        """Initialize base values and state for different sensor types."""
        if self.sensor_type == "temperature":
            self.base_temp = 20.0 + random.uniform(-2.0, 2.0)
        elif self.sensor_type == "humidity":
            self.base_humidity = 55.0 + random.uniform(-5.0, 5.0)
        # elif self.sensor_type == "air_quality":
        #     self.base_air_quality = 50.0 + random.uniform(-10.0, 10.0)
        # elif self.sensor_type == "light":
        #     self.light = 300.0 + random.uniform(-50.0, 50.0)
        elif self.sensor_type == "soil_moisture":
            self.soil_moisture = 50.0 + random.uniform(-5.0, 5.0)
        elif self.sensor_type == "co2":
            self.co2_ppm = 450.0 + random.uniform(-50.0, 50.0)
        else:
            raise ValueError(f"Unknown sensor type: {self.sensor_type}")

    def _now_seconds(self) -> float:
        """Return epoch seconds (float) for time-based functions."""
        return datetime.now(timezone.utc).timestamp()

    def _simulate_temperature(self, t: float) -> float:
        # """
        # Diurnal temperature model:
        #  - base + amplitude * sin(2*pi * (t / period) + phase) + small noise
        # period = 24 hours -> 86400 seconds, Will naturally cross 10–35°C range to allow Node-RED alerts.
        # """
        # period = 86400.0  # seconds in a day
        # amplitude = 10.0
        # # phase shift so peak occurs around 15:00 UTC (approx warmest hour)
        # phase = 2.0
        # temp = self.base_temp + amplitude * math.sin(2 * math.pi * (t / period) + phase)
        # temp += random.uniform(-0.5, 0.5)  # small measurement noise
        # return round(temp, 2)
        """
        Temperature with more aggressive swings to trigger alerts every ~30 sec.
        Cycles between normal and critical states.
        """
        # Cycle pattern: normal (5 readings) -> warning (2 readings) -> critical (1 reading) -> repeat
        cycle_len = 6
        cycle_pos = self._reading_count % cycle_len
        cycle_num = (self._reading_count // cycle_len)
        low_cycle = (cycle_num % 2 == 0)

        if cycle_pos < 4:
            # Normal range 18-22°C
            temp = self.base_temp + random.uniform(-1.0, 1.0)
        elif cycle_pos == 4:
            # Warning: low or high depending on cycle parity
            if low_cycle:
                temp = 13.0 + random.uniform(-1.0, 1.0)   # warning low
            else:
                temp = 30.0 + random.uniform(-2.0, 2.0)   # warning high
        else:  # cycle_pos == 5 -> immediate critical same polarity
            if low_cycle:
                temp = 8.0 + random.uniform(-1.0, 1.5)    # critical low
            else:
                temp = 36.0 + random.uniform(-1.0, 2.0)   # critical high

        return round(temp, 2)

    def _simulate_humidity(self, t: float) -> float:
        # """
        # Humidity generally inversely correlated with temperature with additional noise.
        # """
        # temp_component = -5.0 * math.sin(2 * math.pi * (t / 86400.0) + 2.0)
        # humidity = self.base_humidity + temp_component + random.uniform(-2.0, 2.0)
        # humidity = min(max(humidity, 0.0), 100.0)
        # return round(humidity, 2)
        """
        Humidity with cycles to trigger alerts every ~30 sec.
        """
        cycle_len = 6
        cycle_pos = self._reading_count % cycle_len
        cycle_num = (self._reading_count // cycle_len)
        low_cycle = (cycle_num % 2 == 0)

        if cycle_pos < 4:
            humidity = self.base_humidity + random.uniform(-2.0, 2.0)
        elif cycle_pos == 4:
            if low_cycle:
                humidity = 27.0 + random.uniform(-2.0, 2.0)   # warning low
            else:
                humidity = 82.0 + random.uniform(-3.0, 3.0)   # warning high
        else:
            if low_cycle:
                humidity = 18.0 + random.uniform(-3.0, 2.0)   # critical low
            else:
                humidity = 92.0 + random.uniform(-2.0, 5.0)   # critical high

        humidity = min(max(humidity, 0.0), 100.0)
        return round(humidity, 2)
    
    # def _simulate_air_quality(self) -> float:
    #     """
    #     Air Quality Index (AQI) simulation.
    #     Generates smooth variation with occasional spikes.
    #     """
    #     # Base drift
    #     self.base_air_quality += random.uniform(-2.0, 2.0)
    #     # occasional pollution spike
    #     if random.random() < 0.02:
    #         self.base_air_quality += random.uniform(20.0, 60.0)
    #     # clamp between 0 and 500
    #     self.base_air_quality = min(max(self.base_air_quality, 0.0), 500.0)
    #     return round(self.base_air_quality, 1)

    # def _simulate_light(self, t: float) -> float:
    #     """
    #     Light model: 0 at night, peaks at daytime. Use absolute value of sine to get daylight shape.
    #     Add random cloudiness factor.
    #     """
    #     # faster cycle for demo (optional). For realistic daily cycle leave denominator 86400.
    #     # We keep 86400 to preserve realism.
    #     daylight = max(0.0, math.sin(2 * math.pi * (t / 86400.0) - 1.0))
    #     cloudiness = random.uniform(0.6, 1.0)  # 1.0 = clear sky, 0.6 = cloudy
    #     lux = max(0.0, (self.light * 2.0) * daylight * cloudiness + random.uniform(-20, 20))
    #     return round(lux, 1)

    def _simulate_soil_moisture(self) -> float:
        # """
        # Soil moisture drifts slowly. Simulate small evaporation changes plus occasional random events.
        # """
        # # small random walk
        # self.soil_moisture += random.uniform(-0.5, 0.5)
        # # occasional drying burst
        # if random.random() < 0.02:
        #     self.soil_moisture -= random.uniform(3.0, 7.0)
        # # occasional watering (big jump)
        # if random.random() < 0.01:
        #     self.soil_moisture += random.uniform(6.0, 15.0)
        # # clamp
        # self.soil_moisture = min(max(self.soil_moisture, 0.0), 100.0)
        # return round(self.soil_moisture, 2)
        """
        Soil moisture with aggressive cycles to trigger alerts every ~30 sec.
        """
        cycle_len = 6
        cycle_pos = self._reading_count % cycle_len
        cycle_num = (self._reading_count // cycle_len)
        low_cycle = (cycle_num % 2 == 0)

        if cycle_pos < 4:
            self.soil_moisture = 50.0 + random.uniform(-5.0, 5.0)
        elif cycle_pos == 4:
            if low_cycle:
                self.soil_moisture = 30.0 + random.uniform(-5.0, 5.0)   # warning low
            else:
                self.soil_moisture = 75.0 + random.uniform(-5.0, 5.0)   # warning high
        else:
            if low_cycle:
                self.soil_moisture = 15.0 + random.uniform(-5.0, 5.0)   # critical low
            else:
                self.soil_moisture = 92.0 + random.uniform(-2.0, 5.0)   # critical high

        self.soil_moisture = min(max(self.soil_moisture, 0.0), 100.0)
        return round(self.soil_moisture, 2)
    
    def _simulate_co2(self) -> float:
        # """
        # CO2 simulation in ppm.
        # - slow drift around base
        # - occasional occupancy spikes (e.g., indoors)
        # - occasional ventilation drops
        # """
        # # small drift
        # self.co2_ppm += random.uniform(-8.0, 8.0)
        # # occupancy spike
        # if random.random() < 0.04:
        #     self.co2_ppm += random.uniform(100.0, 400.0)
        # # long stagnation (CO2 rises slowly)
        # if random.random() < 0.02:
        #     self.co2_ppm += random.uniform(30.0, 120.0)
        # # fresh air event
        # if random.random() < 0.015:
        #     self.co2_ppm -= random.uniform(50.0, 200.0)
        # # clamp to realistic bounds
        # self.co2_ppm = min(max(self.co2_ppm, 350.0), 5000.0)
        # return round(self.co2_ppm, 1)
        """
        CO2 with cycles to trigger critical alerts every ~30 sec.
        """
        cycle_len = 6
        cycle_pos = self._reading_count % cycle_len
        cycle_num = (self._reading_count // cycle_len)
        low_cycle = (cycle_num % 2 == 0)

        if cycle_pos < 4:
            self.co2_ppm = 500.0 + random.uniform(-50.0, 50.0)
        elif cycle_pos == 4:
            if low_cycle:
                self.co2_ppm = 320.0 + random.uniform(-20.0, 10.0)   # warning low
            else:
                self.co2_ppm = 1300.0 + random.uniform(-50.0, 100.0) # warning high
        else:
            if low_cycle:
                self.co2_ppm = 250.0 + random.uniform(-30.0, 30.0)   # critical low (synthetic)
            else:
                # critical high / spike
                # sometimes produce extreme on alternate high-critical cycles
                if (cycle_num % 4) == 1:
                    self.co2_ppm = 3200.0 + random.uniform(-200.0, 500.0)  # extreme
                else:
                    self.co2_ppm = 2500.0 + random.uniform(-200.0, 300.0)  # critical high

        self.co2_ppm = min(max(self.co2_ppm, 200.0), 5000.0)
        return round(self.co2_ppm, 1)
    
    def generate_reading(self) -> str:
        """
        Build a JSON payload containing:
         - device_id
         - timestamp (ISO 8601 UTC)
         - readings: {temperature, humidity, light, soil_moisture}
        Returns a JSON-encoded string ready for MQTT publish.
        """
        t = self._now_seconds()

        if self.sensor_type == "temperature":
            value = self._simulate_temperature(t)
        elif self.sensor_type == "humidity":
            value = self._simulate_humidity(t)
        # elif self.sensor_type == "air_quality":
        #     value = self._simulate_air_quality()
        # elif self.sensor_type == "light":
        #     value = self._simulate_light(t)
        elif self.sensor_type == "soil_moisture":
            value = self._simulate_soil_moisture()
        elif self.sensor_type == "co2":
            value = self._simulate_co2()
        else:
            raise ValueError(f"Unsupported sensor type: {self.sensor_type}")
        
        self._reading_count += 1

        payload = {
            "device_id": self.device_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sensor_type": self.sensor_type,
            "value": value,
        }
        # return as a compact JSON string
        return json.dumps(payload, separators=(",", ":"))

"""
SensorSimulator: produce realistic synthetic sensor readings.

This module implements:
 - realistic diurnal (sinusoidal) variation for temperature and light,
 - smoother drift for soil moisture and humidity,
 - ability to generate a JSON payload ready for MQTT.

The generator is deterministic enough for reproducible scenarios but adds
random noise and optional device-specific offsets.
"""