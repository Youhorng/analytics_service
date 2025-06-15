import logging
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

from app.config.config import settings

# Global database client and db
client = None
db = None

async def connect_to_mongodb():
    """Connect to MongoDB and initialize the client"""
    global client, db
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DB]
        
        # Verify connection
        await client.admin.command('ping')
        logging.info(f"Connected to MongoDB: {settings.MONGODB_URI}")
        
        # Return the database connection
        return db
    except ConnectionFailure as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise e
    except Exception as e:
        logging.error(f"Unexpected error connecting to MongoDB: {e}")
        raise e

async def close_mongodb_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        logging.info("MongoDB connection closed")

# Export the database object
def get_db():
    """Get the database connection"""
    global db
    if db is None:
        raise ValueError("Database connection not initialized")
    return db