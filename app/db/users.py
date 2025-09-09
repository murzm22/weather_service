from fastapi import HTTPException, Depends
from app.db.mongo import users_collection
from app.db.security import get_password_hash, verify_password
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


async def create_user(username: str, password: str): # регистрация
    existing = await users_collection.find_one({"username": username})
    if existing:
        raise HTTPException(status_code=409, detail="Пользователь уже существует")
    hashed_password = get_password_hash(password)
    user = {"username": username, "password": hashed_password}
    await users_collection.insert_one(user)
    return {"msg": f"Пользователь {username} зарегистрирован"}



async def authenticate_user(username: str, password: str): # аутентификация
    user = await users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return None
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)): # получаем текущего пользователя по токену
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
        user = await users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")