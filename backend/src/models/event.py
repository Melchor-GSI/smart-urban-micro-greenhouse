from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class Event(BaseModel):
    id: Optional[str] = None
    sensor: str
    location: str
    creation_date: Optional[datetime] = None

    @model_validator(mode="after")
    def set_creation_time(self) -> "Event":
        if not self.creation_date:
            self.creation_date = datetime.now()
        return self
