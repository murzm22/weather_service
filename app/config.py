from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    CITY_URL: str = "https://nominatim.openstreetmap.org/search"
    SECRET_KEY: str
    ALGORITHM: str
    MONGO_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()