from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class Reading(BaseModel):
    id: Optional[str] = None
    variable: Literal["temperature", "humidity", "air_quality"]
    sensor: str
    value: float
    creation_date: Optional[datetime] = None

    @model_validator(mode="after")
    def set_creation_time(self) -> "Reading":
        if not self.creation_date:
            self.creation_date = datetime.now()
        return self
