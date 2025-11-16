from typing import Optional

from src.config.database import db
from src.models.event import Event


class EventService:
    def __init__(self):
        self.serializer = Event
        self.collection_name = "events"

    def get_items(self, status: Optional[str] = None):
        """
        Get events with optional status filtering

        Args:
            status: Filter by specific status (active, acknowledged, resolved).
                   If None, returns all events.

        Returns:
            List of Event objects matching the filter criteria
        """
        # Build query filter
        query_filter = {}

        if status:
            query_filter["status"] = status

        # Execute query and sort by creation date (most recent first)
        events = (
            db.get_collection(self.collection_name)
            .find(query_filter)
            .sort("creation_date", -1)
        )

        return [self.serializer.model_validate(event) for event in events]

    def set_item(self, item):
        try:
            events_collection = db.get_collection(self.collection_name)
            events_collection.insert_one(item.model_dump())
            return True
        except Exception as e:
            print(f"Error inserting event: {e}")
            return False

    def active_event(self, event):
        """
        Check if there's an active or acknowledged event with the same variable and event_type

        Args:
            event: Event object to check against

        Returns:
            Event object if found, None otherwise
        """
        try:
            query_filter = {
                "variable": event.variable,
                "event_type": event.event_type,
                "status": {"$in": ["active", "acknowledged"]},
            }

            events_collection = db.get_collection(self.collection_name)
            existing_event = events_collection.find_one(query_filter)

            if existing_event:
                return self.serializer.model_validate(existing_event)

            return None

        except Exception as e:
            print(f"Error checking for active event: {e}")
            return None

    def patch_item(self, id, item):
        try:
            events_collection = db.get_collection(self.collection_name)
            result = events_collection.update_one({"id": id}, {"$set": item})
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating event: {e}")
            return False
