from app.config import OPENWEATHER_API_KEY, BASE_URL
import aiohttp
import asyncio


# coords = [
#     (55.75, 37.61),  # Москва
#     (59.93, 30.31),  # СПБ
#     (47.23, 39.72),   # Ростов
# ]

coords = []  # ввод пользователем координат
while True:
    lat = input("Введите широту (или Enter для завершения): ")
    if not lat:
        break
    lon = input("Введите долготу: ")
    coords.append((float(lat), float(lon)))

async def get_weather(coords):
    tasks =[]
    async with aiohttp.ClientSession() as session:
        for lat, lon in coords:
            tasks.append(session.get(BASE_URL, params={
                "lat": lat, "lon": lon,
                "appid": OPENWEATHER_API_KEY,
                "units": "metric",
                "lang": "ru"
            }))
        r = await asyncio.gather(*tasks)

        result = []
        for res in r:
            result.append(await res.json())
        return result

async def main():
    data = await get_weather(coords)
    for weather in data:
        city = weather ["name"]
        temp = weather ["main"]["temp"]
        tempo =  weather ["main"]["feels_like"]
        desc =  weather ["weather"][0]["description"]
        print(f"{city}: {temp}°C, ощущается как {tempo}°C, {desc}")

asyncio.run(main())





