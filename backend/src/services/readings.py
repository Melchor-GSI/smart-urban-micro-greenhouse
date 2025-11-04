from src.config.database import db
from src.models.reading import Reading


class ReadingService:
    def __init__(self):
        self.serializer = Reading
        self.collection_name = "readings"

    def get_items(self):
        readings = db.get_collection(self.collection_name).find().sort("timestamp", -1)
        return [self.serializer.model_validate(reading) for reading in readings]
