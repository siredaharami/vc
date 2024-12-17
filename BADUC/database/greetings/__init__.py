from sys import exit as exiter
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging

from BADUC.core.config import MONGO_DB_URL, DB_NAME

# Configure logging for the userbot
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UserbotLogger")

try:
    # Initialize MongoDB client
    userbot_db_client = MongoClient(MONGO_DB_URL)
except PyMongoError as e:
    logger.error(f"Error connecting to MongoDB: {e}")
    exiter(1)

# Reference the database
userbot_main_db = userbot_db_client[DB_NAME]

class MongoDB:
    """Helper class for interacting with MongoDB for the userbot."""

    def __init__(self, collection_name):
        """Initialize with the specified collection."""
        self.collection = userbot_main_db[collection_name]

    def insert_one(self, document):
        """Insert a single document into the collection."""
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def find_one(self, query):
        """Find a single document matching the query."""
        result = self.collection.find_one(query)
        return result if result else None

    def find_all(self, query=None):
        """Find all documents matching the query."""
        if query is None:
            query = {}
        return list(self.collection.find(query))

    def count(self, query=None):
        """Count the number of documents matching the query."""
        if query is None:
            query = {}
        return self.collection.count_documents(query)

    def delete_one(self, query):
        """Delete documents matching the query."""
        self.collection.delete_many(query)
        return self.collection.count_documents({})

    def replace(self, query, new_data):
        """Replace a single document matching the query with new data."""
        old_document = self.collection.find_one(query)
        if not old_document:
            return None, None
        _id = old_document["_id"]
        self.collection.replace_one({"_id": _id}, new_data)
        new_document = self.collection.find_one({"_id": _id})
        return old_document, new_document

    def update(self, query, update_data):
        """Update a single document matching the query."""
        result = self.collection.update_one(query, {"$set": update_data})
        updated_document = self.collection.find_one(query)
        return result.modified_count, updated_document

    @staticmethod
    def close():
        """Close the database connection."""
        userbot_db_client.close()


def initialize_database():
    """Test MongoDB connection on userbot startup."""
    try:
        test = MongoDB("test")
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        exiter(1)


# Call initialization during userbot startup
initialize_database()
