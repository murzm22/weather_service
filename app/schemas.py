from typing import List
from pydantic import BaseModel


class WeatherResponse(BaseModel): # для вывода погоды
    city: str
    temperature: float
    feels_like: float
    description: str

class CitiesRequest(BaseModel): # для получения погоды по городам
    cities: List[str]

class User(BaseModel): # в регистрации
    username: str
    password: str

class Location(BaseModel):  # для удаления координат
    lat: float
    lon: float

class LocationUpdate(BaseModel): # для обновления координат в БД
    old_lat: float
    old_lon: float
    new_lat: float
    new_lon: float

class CityNames(BaseModel): # # для добавления широты\долготы городов
    cities: list[str]