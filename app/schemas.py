from typing import List, Tuple, Optional
from beanie import Document
from bson import ObjectId
from pydantic import BaseModel, Field


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