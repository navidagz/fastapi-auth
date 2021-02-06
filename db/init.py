import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase

from config.settings import settings
from .schema import UserDB

DATABASE_URL = settings.mongo_url
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["auth"]
collection = db["users"]

user_db = MongoDBUserDatabase(UserDB, collection)
