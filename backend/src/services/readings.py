from datetime import datetime, timedelta
from typing import Optional

from src.config.database import db
from src.models.reading import Reading


class ReadingService:
    def __init__(self):
        self.serializer = Reading
        self.collection_name = "readings"

    def get_items(
        self,
        now: bool = False,
        variable: Optional[str] = None,
        hours_back: Optional[int] = None,
    ):
        """
        Get readings with optional filtering

        Args:
            now: If True, get latest reading for each variable
            variable: Filter by specific variable
            hours_back: Get readings from the last N hours
        """
        if now:
            pipeline = [
                {"$sort": {"creation_date": -1}},
                {
                    "$group": {
                        "_id": "$variable",
                        "latest_reading": {"$first": "$$ROOT"},
                    }
                },
                {"$replaceRoot": {"newRoot": "$latest_reading"}},
            ]
            readings = db.get_collection(self.collection_name).aggregate(pipeline)
            return [self.serializer.model_validate(reading) for reading in readings]

        # Build query filter
        query_filter = {}

        if variable:
            query_filter["variable"] = variable

        if hours_back:
            time_threshold = datetime.now() - timedelta(hours=hours_back)
            query_filter["creation_date"] = {"$gte": time_threshold}

        # Execute query
        readings = (
            db.get_collection(self.collection_name)
            .find(query_filter)
            .sort("creation_date", -1)
        )

        return [self.serializer.model_validate(reading) for reading in readings]
