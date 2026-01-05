from typing import Optional, Any
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    client: Optional[Any] = None
    database: Optional[Any] = None


db = Database()


async def connect_to_mongo():
    from motor.motor_asyncio import AsyncIOMotorClient
    
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_database = os.getenv("MONGODB_DATABASE", "Valdeci")
    
    db.client = AsyncIOMotorClient(mongodb_uri)
    db.database = db.client[mongodb_database]


async def close_mongo_connection():
    if db.client:
        db.client.close()


def get_database() -> Any:
    return db.database
