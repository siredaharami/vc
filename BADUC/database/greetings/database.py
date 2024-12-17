from pymongo import MongoClient
from pymongo.errors import PyMongoError
from BADUC.core.config import MONGO_DB_URL, DB_NAME  # Update the paths to your config file

class MongoDB:
    """Helper class to interact with MongoDB collections."""

    def __init__(self, collection_name: str):
        """Initialize MongoDB connection and select the collection."""
        try:
            self.client = MongoClient(MONGO_DB_URL)
            self.db = self.client[DB_NAME]
            self.collection = self.db[collection_name]
        except PyMongoError as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")

    def insert_one(self, document: dict):
        """Insert a single document into the collection."""
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def find_one(self, query: dict):
        """Find a single document in the collection."""
        return self.collection.find_one(query)

    def find_all(self, query: dict = None):
        """Find all documents matching the query."""
        query = query or {}
        return list(self.collection.find(query))

    def update(self, query: dict, update_data: dict):
        """Update a single document matching the query."""
        result = self.collection.update_one(query, {"$set": update_data})
        return result.modified_count, self.find_one(query)

    def delete_one(self, query: dict):
        """Delete documents matching the query."""
        self.collection.delete_one(query)

    def count(self, query: dict = None) -> int:
        """Count documents matching the query."""
        query = query or {}
        return self.collection.count_documents(query)

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()
