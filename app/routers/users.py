from fastapi import APIRouter, HTTPException, Depends
from app.schemas import AuthData, User
from app.db.users import create_user, authenticate_user, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from app.config import settings
from jose import jwt

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register") # регистрация
async def register(user: AuthData) -> dict:
    return await create_user(user.username, user.password)

@router.post("/login")  # вход с токеном
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    db_user = await authenticate_user(form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": form_data.username, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/Delete")
async def delete(user: User = Depends(get_current_user)):
    await user.delete()