from fastapi import HTTPException
from app.db.mongo import users_collection
from app.db.db import get_password_hash, verify_password

async def create_user(username: str, password: str):
    existing = await users_collection.find_one({"username": username})
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = get_password_hash(password)
    user = {"username": username, "password": hashed_password}
    await users_collection.insert_one(user)
    return {"msg": f"Пользователь {username} зарегистрирован"}

async def authenticate_user(username: str, password: str):
    user = await users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None
    return user