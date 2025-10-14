import redis.asyncio as redis

redis_client = redis.from_url("redis://redis:6379", decode_responses=True)

async def set_cache(key: str, value: str, ttl: 300):
    await redis_client.set(key, value,ex=ttl)

async def get_cache(key: str):
    return await redis_client.get(key)