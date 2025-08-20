import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"