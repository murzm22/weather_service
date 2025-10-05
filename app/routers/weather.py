from fastapi import Query, Body, Depends, APIRouter
from app.schemas import WeatherResponse, CitiesRequest, User
from app.weather.async_client import get_weather_by_coords, get_multi_weather_by_coords, get_multi_coords_by_city, parse_weather_data
from typing import List, Tuple
from app.db.users import get_current_user


router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/by_coords") # Одиночный запрос по координатам
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

@router.post("/by_coords/multi") # Массовый запрос по координатам
async def multi_weather_by_coords(
        coords: List[Tuple[float, float]] = Body(...)
)-> List[WeatherResponse]:
    data = await get_multi_weather_by_coords(coords)
    return parse_weather_data(data)


@router.post("/by_city/multi") # Массовый запрос по городам
async def weather_by_city_multi(cities_request: CitiesRequest = Body(...)):
    coords = await get_multi_coords_by_city(cities_request.cities)
    data = await get_multi_weather_by_coords(coords)
    return parse_weather_data(data)

@router.get("/users/by_save_coords")  # Получение погоды по сохранённым локациям
async def  get_users_weather_by_coords(current_user: User = Depends(get_current_user)) -> List[WeatherResponse] | dict:
    if not current_user.locations:
        return {"msg": "У пользователя нет сохранённых локаций"}
    coords = [(loc.lat, loc.lon) for loc in current_user.locations]
    data = await get_multi_weather_by_coords(coords)
    return parse_weather_data(data)