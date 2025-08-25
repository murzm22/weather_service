from typing import List
from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    feels_like: float
    description: str

class CitiesRequest(BaseModel):
    cities: List[str]
