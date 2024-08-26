from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()


MONGO_DB_URL = os.getenv("MONGO_DB_URL")

client = AsyncIOMotorClient(MONGO_DB_URL)
db = client.your_database_name  # Replace with your database name


def get_user_collection():
    return db.users
