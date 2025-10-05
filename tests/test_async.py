import pytest, re
from aioresponses import aioresponses
from app.weather.async_client import get_weather_by_coords, get_multi_weather_by_coords, get_multi_coords_by_city


@pytest.mark.asyncio
async def test_get_weather_by_coords():
    lat, lon = 55.75, 37.61

    fake_response = {
        "weather":[{"description": "Пасмурно"}],
        "main":{"temp":5}
    }

    with aioresponses() as mocked:
        mocked.get(
            re.compile(r"https://api\.openweathermap\.org/data/2\.5/weather.*"),
            payload=fake_response
        )
        result = await get_weather_by_coords(lat, lon)

        assert "weather" in result
        assert result["main"]["temp"] == 5
        assert result["weather"][0]["description"] == "Пасмурно"


@pytest.mark.asyncio
async def test_get_multi_weather_by_coords():
    coords = [(55.75, 37.61), (59.93, 30.33)]

    fake_response = [
        {"weather":[{"description": "Пасмурно"}], "main":{"temp":5}},
        {"weather": [{"description": "Дождь"}], "main": {"temp": 3}}
    ]

    with aioresponses() as mocked:
        for response in fake_response:
            mocked.get(
                re.compile(r"https://api\.openweathermap\.org/data/2\.5/weather.*"),
                payload=response,
                repeat=False
            )

        results = await get_multi_weather_by_coords(coords)

        assert len(results) == 2
        assert results[0]["main"]["temp"] == 5
        assert results[0]["weather"][0]["description"] == "Пасмурно"
        assert results[1]["main"]["temp"] == 3
        assert results[1]["weather"][0]["description"] == "Дождь"

@pytest.mark.asyncio
async def test_get_multi_coords_by_city():
    cities= ["Москва", "Ростов"]

    fake_response = [
        [{"lat": "55.625578", "lon": "37.6063916"}],
        [{"lat": "47.2216548", "lon": "39.7096061"}]
    ]

    with aioresponses() as mocked:
        for name, response in cities, fake_response:
            mocked.get(
                re.compile(r"https://nominatim.openstreetmap.org/search.*"),
                payload=response,
                repeat=False
            )

    results = await get_multi_coords_by_city(cities)

    assert len(results) == 2
    assert results[0] == (55.625578, 37.6063916)
    assert results[1] == (47.2216548, 39.7096061)