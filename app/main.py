import fastapi
from fastapi import Query, Body
from typing import List, Tuple
from app.weather.async_client import get_weather, get_multi_weather


app=fastapi.FastAPI()

@app.get("/weather")
async def weather(
        lat: float = Query(...),
        lon: float = Query(...)):
    data = await get_weather(lat, lon)
    return {
        "city": data.get("name"),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "description": data["weather"][0]["description"]
    }

@app.post("/weather/multi")
async def multi_weather(coords: List[Tuple[float, float]] = Body(...)):
    data = await get_multi_weather(coords)
    result = []
    for w in data:
        if w:
            result.append({
                "city": w.get("name"),
                "temperature": w["main"]["temp"],
                "feels_like": w["main"]["feels_like"],
                "description": w["weather"][0]["description"]
            })
    return result