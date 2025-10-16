from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from app.db.mongo import init_db, close_db
from app.routers import weather, users, user_locations


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()
app = FastAPI(lifespan=lifespan)

app.include_router(weather.router)

app.include_router(users.router)

app.include_router(user_locations.router)



templates = Jinja2Templates(directory="app/templates")



