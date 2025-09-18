import fastapi
from fastapi import Query, Body, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Tuple
from app.weather.async_client import get_weather_by_coords, get_multi_weather_by_coords, get_multi_weather_by_city, parse_weather_data
from app.schemas import WeatherResponse, CitiesRequest, AuthData, Location, CityNames, LocationUpdate, User
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.db.users import create_user, authenticate_user, get_current_user
from app.config import settings

app=fastapi.FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def on_startup():
    from app.db.mongo import init_db
    await init_db()

@app.get("/", response_class=HTMLResponse) # пробник
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/weather/by_coords") # Одиночный запрос по координатам
async def weather_by_coords(
        lat: float = Query(...),
        lon: float = Query(...)
) -> WeatherResponse:
    data = await get_weather_by_coords(lat, lon)
    return WeatherResponse(
        city=data.get("name"),
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        description=data["weather"][0]["description"]
    )

@app.post("/weather/by_coords/multi") # Массовый запрос по координатам
async def multi_weather_by_coords(
        coords: List[Tuple[float, float]] = Body(...)
)-> List[WeatherResponse]:
    data = await get_multi_weather_by_coords(coords)
    return parse_weather_data(data)

@app.post("/weather/by_city/multi") # Массовый запрос по городам
async def weather_by_city_multi(cities_request: CitiesRequest = Body(...)):
    coords = await get_multi_weather_by_city(cities_request.cities)
    data = await get_multi_weather_by_coords(coords)
    return parse_weather_data(data)

@app.get("/weather/users/by_save_cords")  # Получение погоды по сохранённым локациям
async def  get_users_weather_by_coords(current_user: User = Depends(get_current_user)) -> List[WeatherResponse] | dict:
    if not current_user.locations:
        return {"msg": "У пользователя нет сохранённых локаций"}
    coords = [(loc.lat, loc.lon) for loc in current_user.locations]
    data = await get_multi_weather_by_coords(coords)
    return parse_weather_data(data)

@app.post("/register") # регистрация
async def register(user: AuthData) -> dict:
    return await create_user(user.username, user.password)

@app.post("/login")  # вход с токеном
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    db_user = await authenticate_user(form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": form_data.username, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/Delete")
async def delete(user: User = Depends(get_current_user)):
    await user.delete()

@app.post("/users/locations/add")  # добавление координат городов
async def add_locations(cities: CityNames, current_user: User = Depends(get_current_user)) -> dict:
    locations = await get_multi_weather_by_city(cities.cities)
    if not locations:
        return {"msg": "Ни одна локация не найдена"}
    current_user.locations.extend([Location(lat=lat, lon=lon) for lat, lon in locations])
    await current_user.save()
    return {"msg": f"Добавлено {len(locations)} локаций"}

@app.get("/users/locations/show") # вывод сохраненных координат
async def get_locations(current_user: User = Depends(get_current_user)):
    return current_user.locations or []

@app.put("/users/locations/update") # обновление сохраненных координат
async def update_location(update: LocationUpdate, current_user: User = Depends(get_current_user)):
    if not current_user.locations:
        return {"msg": "У пользователя нет сохранённых локаций"}
    for idx, loc in enumerate(current_user.locations):
        if loc.lat == update.old_lat and loc.lon == update.old_lon:
            current_user.locations[idx] = Location(lat=update.new_lat, lon=update.new_lon)
            await current_user.save()
            return {"msg": "Локация обновлена"}
    return {"msg": "Локация обновлена"}

@app.delete("/users/locations/delete") # удаление координат
async def delete_location(location: Location, current_user: User = Depends(get_current_user)):
    if not current_user.locations:
        return {"msg": "У пользователя нет сохранённых локаций"}
    current_user.locations = [
        loc for loc in current_user.locations
        if not (loc.lat == location.lat and loc.lon == location.lon)
    ]
    await current_user.save()
    return {"msg": "Локация удалена"}