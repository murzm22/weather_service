import asyncio
import aiohttp
from app.config import settings
from app.schemas import WeatherResponse
from typing import List, Dict


async def get_weather_by_coords(lat: float, lon:float):
    async with aiohttp.ClientSession() as session:
            async with session.get(settings.BASE_URL, params={
                "lat": lat, "lon": lon,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "ru"
            }) as response:
                return await response.json()



async def get_multi_weather_by_coords(coords):
    tasks = [
        asyncio.create_task(get_weather_by_coords(lat, lon))
        for lat, lon in coords
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def get_multi_coords_by_city(coords):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for city_name in coords:
            tasks.append(session.get(settings.CITY_URL, params={
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


def parse_weather_data(data: List[Dict]) -> List[WeatherResponse]:
    result: List[WeatherResponse] = []
    for w in data:
        result.append(
            WeatherResponse(
                city=w.get("name"),
                temperature=w["main"]["temp"],
                feels_like=w["main"]["feels_like"],
                description=w["weather"][0]["description"]
            )
        )
    return result
