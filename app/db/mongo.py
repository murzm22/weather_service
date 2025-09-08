from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

MONGO_URL = settings.MONGO_URL
client = AsyncIOMotorClient(MONGO_URL)
db = client["weather_service"]  # база данных
users_collection = db["users"]  # коллекция для пользователей