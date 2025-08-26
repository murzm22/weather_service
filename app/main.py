import fastapi
from fastapi import Query, Body, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Tuple
from app.weather.async_client import get_weather, get_multi_weather, multi_city
from app.schemas import WeatherResponse, CitiesRequest, User
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from datetime import datetime, timedelta
from app.auth.auth import create_user, authenticate_user

app=fastapi.FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse) # HTML каркас
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weather") # Одиночный запрос по координатам
async def weather(
        lat: float = Query(...),
        lon: float = Query(...)):
    data = await get_weather(lat, lon)
    return WeatherResponse(
        city=data.get("name"),
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        description=data["weather"][0]["description"]
    )

@app.post("/weather/multi") # Массовый запрос по координатам
async def multi_weather(coords: List[Tuple[float, float]] = Body(...)):
    data = await get_multi_weather(coords)
    result = []
    for w in data:
            result.append(
                WeatherResponse
                    (
                    city=w.get("name"),
                    temperature=w["main"]["temp"],
                    feels_like=w["main"]["feels_like"],
                    description=w["weather"][0]["description"]
                    )
            )
    return result


@app.post("/weather/city") # Массовый запрос по городам
async def weather_for_city(cities_request: CitiesRequest = Body(...)):
    coords = await multi_city(cities_request.cities)
    data = await get_multi_weather(coords)
    result = []
    for w in data:
        result.append(
            WeatherResponse
                (
                city=w.get("name"),
                temperature=w["main"]["temp"],
                feels_like=w["main"]["feels_like"],
                description=w["weather"][0]["description"]
                )
            )
    return result

@app.post("/register")
async def register(user: User):
    return await create_user(user.username, user.password)


@app.post("/login")
async def login(user: User):
    db_user = await authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}