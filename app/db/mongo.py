from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.schemas import User
from app.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(
        database=client["weather_service"],
        document_models=[User],
    )