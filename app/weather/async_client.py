import asyncio

from app.config import OPENWEATHER_API_KEY, BASE_URL
import aiohttp


async def get_weather(lat: float, lon:float):
    async with aiohttp.ClientSession() as session:
            async with session.get(BASE_URL, params={
                "lat": lat, "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "ru"
            }) as response:
                return await response.json()



async def get_multi_weather(coords):
    tasks =[]
    async with aiohttp.ClientSession() as session:
        for lat, lon in coords:
            tasks.append(session.get(BASE_URL, params={
                "lat": lat, "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "ru"
            }))
        r = await asyncio.gather(*tasks)

        result = []
        for res in r:
            result.append(await res.json())
        return result