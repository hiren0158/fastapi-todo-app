"""
Database initialization and connection management for MongoDB with Beanie ODM.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models_beanie import User, Todo
from .config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager."""
    
    client: AsyncIOMotorClient = None
    
    @classmethod
    async def connect_db(cls):
        """Initialize database connection and Beanie ODM."""
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_url)
            database = cls.client[settings.mongodb_db_name]
            
            await init_beanie(
                database=database,
                document_models=[User, Todo]
            )
            
            logger.info(f"Connected to MongoDB at {settings.mongodb_url}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    @classmethod
    async def close_db(cls):
        """Close database connection."""
        if cls.client:
            cls.client.close()
            logger.info("Closed MongoDB connection")

async def init_db():
    """Initialize database connection."""
    await Database.connect_db()

async def close_db():
    """Close database connection."""
    await Database.close_db()
