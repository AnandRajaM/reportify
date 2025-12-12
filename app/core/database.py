"""
Database connection and utilities
"""
from pymongo import MongoClient
from app.core.config import settings


class Database:
    """MongoDB Database Handler"""
    
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to MongoDB"""
        self.client = MongoClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        return self.db
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
    
    def get_collection(self, collection_name: str = None):
        """Get a collection from the database"""
        if not self.db:
            self.connect()
        collection = collection_name or settings.COLLECTION_NAME
        return self.db[collection]


# Database instance
db = Database()


def get_database():
    """Dependency for database access"""
    if not db.db:
        db.connect()
    return db.db
