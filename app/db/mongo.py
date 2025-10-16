from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.schemas import User
from app.config import settings

client: AsyncMongoClient | None = None

async def init_db():
    global client
    client = AsyncMongoClient(settings.MONGO_URL)
    await init_beanie(
        database=client["weather_service"],
        document_models=[User],
    )

async def close_db():
    global client
    if client is not None:
        client.close()