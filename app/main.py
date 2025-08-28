import fastapi
from fastapi import Query, Body, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Tuple
from app.weather.async_client import get_weather, get_multi_weather, multi_city
from app.schemas import WeatherResponse, CitiesRequest, User, Location, CityNames, LocationUpdate
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.auth.auth import create_user, authenticate_user, get_current_user
from app.db.mongo import users_collection

app=fastapi.FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse) # пробник
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

@app.get("/weather/my")  # Получение погоды по сохранённым локациям
async def my_weather(current_user: dict = Depends(get_current_user)):
    user = await users_collection.find_one({"username": current_user["username"]})
    if not user or "locations" not in user or not user["locations"]:
        return {"msg": "У пользователя нет сохранённых локаций"}
    coords = [(loc["lat"], loc["lon"]) for loc in user["locations"]]
    data = await get_multi_weather(coords)
    result = []
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

@app.post("/register") # регистрация
async def register(user: User):
    return await create_user(user.username, user.password)


# @app.post("/login")
# async def login(user: User):
#     db_user = await authenticate_user(user.username, user.password)
#     if not db_user:
#         raise HTTPException(status_code=401, detail="Неверные учетные данные")
#
#     expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     token = jwt.encode({"sub": user.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
#     return {"access_token": token, "token_type": "bearer"}
@app.post("/login")  # еще раз вникнуть в структуру и принцип передачи токена
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await authenticate_user(form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": form_data.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/locations") # добавление широты\долготы городов
async def add_locations(cities: CityNames, current_user: dict = Depends(get_current_user)):
    locations = await multi_city(cities.cities)
    if not locations:
        return {"msg": "Ни одна локация не найдена"}

    await users_collection.update_one(
        {"username": current_user["username"]},
        {"$push": {"locations": {"$each": locations}}}
    )
    return {"msg": f"Добавлено {len(locations)} локаций"}

@app.get("/locations") # вывод сохраненных координат
async def get_locations(current_user: dict = Depends(get_current_user)):
    user = await users_collection.find_one({"username": current_user["username"]})
    return user.get("locations", [])

@app.put("/locations") # обновление сохраненных координат
async def update_location(update: LocationUpdate, current_user: dict = Depends(get_current_user)):
    await users_collection.update_one(
        {"username": current_user["username"], "locations.lat": update.old_lat, "locations.lon": update.old_lon},
        {"$set": {"locations.$": {"lat": update.new_lat, "lon": update.new_lon}}}
    )
    return {"msg": "Локация обновлена"}

@app.delete("/locations") # удаление координат
async def delete_location(location: Location, current_user: dict = Depends(get_current_user)):
    await users_collection.update_one(
        {"username": current_user["username"]},
        {"$pull": {"locations": {"lat": location.lat, "lon": location.lon,}}}
    )
    return {"msg": "Локация удалена"}

