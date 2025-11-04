import logging
import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logger = logging.getLogger(__name__)


class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self.connect()

    def connect(self):
        try:
            # Get MongoDB configuration from environment variables
            mongodb_uri = os.getenv("MONGODB_URI")

            if mongodb_uri:
                self._client = MongoClient(mongodb_uri)
            else:
                # Fallback to individual environment variables
                host = os.getenv("MONGODB_HOST", "localhost")
                port = int(os.getenv("MONGODB_PORT", 27017))
                username = os.getenv("MONGODB_USERNAME")
                password = os.getenv("MONGODB_PASSWORD")
                database = os.getenv("MONGODB_DATABASE", "iot_db")

                if username and password:
                    self._client = MongoClient(
                        host=host,
                        port=port,
                        username=username,
                        password=password,
                        authSource="admin",
                    )
                else:
                    self._client = MongoClient(host=host, port=port)

            # Test the connection
            self._client.admin.command("ping")

            # Get database
            db_name = os.getenv("MONGODB_DATABASE", "iot_db")
            self._db = self._client[db_name]

            logger.info(f"Successfully connected to MongoDB database: {db_name}")

        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise e

    def get_database(self):
        if self._db is None:
            self.connect()
        return self._db

    def get_collection(self, collection_name):
        db = self.get_database()
        return db[collection_name]

    def close(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None


# Singleton instance
db = Database()
