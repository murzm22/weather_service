from fastapi import APIRouter, Depends
from app.schemas import Location, CityNames, LocationUpdate, User
from app.db.users import get_current_user
from app.weather.async_client import get_multi_coords_by_city

router = APIRouter(prefix="/user/location", tags=["user location"])

@router.post("/add")  # добавление координат городов
async def add_locations(cities: CityNames, current_user: User = Depends(get_current_user)) -> dict:
    locations = await get_multi_coords_by_city(cities.cities)
    if not locations:
        return {"msg": "Ни одна локация не найдена"}
    current_user.locations.extend([Location(lat=lat, lon=lon) for lat, lon in locations])
    await current_user.save()
    return {"msg": f"Добавлено {len(locations)} локаций"}

@router.get("/show") # вывод сохраненных координат
async def get_locations(current_user: User = Depends(get_current_user)):
    return current_user.locations or []

@router.put("/update") # обновление сохраненных координат
async def update_location(update: LocationUpdate, current_user: User = Depends(get_current_user)):
    if not current_user.locations:
        return {"msg": "У пользователя нет сохранённых локаций"}
    for idx, loc in enumerate(current_user.locations):
        if loc.lat == update.old_lat and loc.lon == update.old_lon:
            current_user.locations[idx] = Location(lat=update.new_lat, lon=update.new_lon)
            await current_user.save()
            return {"msg": "Локация обновлена"}
    return {"msg": "Локация обновлена"}

@router.delete("/delete") # удаление координат
async def delete_location(location: Location, current_user: User = Depends(get_current_user)):
    if not current_user.locations:
        return {"msg": "У пользователя нет сохранённых локаций"}
    current_user.locations = [
        loc for loc in current_user.locations
        if not (loc.lat == location.lat and loc.lon == location.lon)
    ]
    await current_user.save()
    return {"msg": "Локация удалена"}

