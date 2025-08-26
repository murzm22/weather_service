import asyncio
from app.config import OPENWEATHER_API_KEY, BASE_URL, CITY_URL
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
    async with aiohttp.ClientSession() as session:
        tasks = []
        for lat, lon in coords:
            tasks.append(session.get(BASE_URL, params={
                "lat": lat, "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "ru"
            }))
        responses = await asyncio.gather(*tasks)
        result = []
        for res in responses:
            result.append(await res.json())
    return result


async def multi_city(coords):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city_name in coords:
            tasks.append(session.get(CITY_URL, params={
                "q": city_name,
                "format": "json",
                "limit": 1
            }))
        responses = await asyncio.gather(*tasks)
        result = []
        for res in responses:
            data = await res.json()
            result.append((float(data[0]["lat"]), float(data[0]["lon"])))
    return result



