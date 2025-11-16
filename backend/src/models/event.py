from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class Event(BaseModel):
    id: Optional[str] = None
    sensor: str
    variable: Literal["temperature", "humidity", "soil_moisture", "co2"]
    event_type: Literal[
        "over_limit", "under_limit", "warning_bottom", "warning_top", "disconnected"
    ]
    urgency: Literal["low", "medium", "high"]
    status: Literal["active", "acknowledged", "resolved"]
    creation_date: Optional[datetime] = None

    @model_validator(mode="after")
    def set_creation_time(self) -> "Event":
        if not self.creation_date:
            self.creation_date = datetime.now()
        return self
