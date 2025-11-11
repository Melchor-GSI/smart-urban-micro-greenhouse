from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, model_validator

VARIABLE_TYPES = Literal["temperature", "humidity", "soil_moisture", "co2"]


class Reading(BaseModel):
    id: Optional[str] = None
    variable: VARIABLE_TYPES
    sensor: str
    value: float
    creation_date: Optional[datetime] = None

    @model_validator(mode="after")
    def set_creation_time(self) -> "Reading":
        if not self.creation_date:
            self.creation_date = datetime.now()
        return self


class ReadingsResponse(BaseModel):
    timestamp: Optional[datetime] = None
    temperature: float
    humidity: float
    soil_moisture: float
    co2: float

    @model_validator(mode="after")
    def set_timestamp(self) -> "ReadingsResponse":
        if not self.timestamp:
            self.timestamp = datetime.now()
        return self
