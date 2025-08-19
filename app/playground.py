import requests

coords = [
    ("Москва", 55.75, 37.61),
    ("СПБ", 59.93, 30.31),
    ("Париж", 48.85, 2.35)
]

api_key = "d4ad52155d675aa6c69fcd7ce0bf57e6"

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric", "lang": "ru"}
    r = requests.get(url, params=params)
    return r.json()


for city, lat, lon in coords:
    data = get_weather(lat, lon)
    temp = data["main"]["temp"]
    tempo = data["main"]["feels_like"]
    desc = data["weather"][0]["description"]
    print(f"{city}: {temp}°C, ощущается как {tempo}°C, {desc}")