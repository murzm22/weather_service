# Weather Service - Асинхронный веб-сервис погоды на FastAPI

## Описание проекта

Weather Service - пет-проект, созданный для изучения веб разработки на Python.  
Основные функции сервиса :
- регистрирация и авторизация пользователей;
- работа с координатами (CRUD);
- получение погодных данных;
- работа через асинхронные запросы к OpenWeather API.

## Технологии и стек

- **Python 3.13**
- **FastAPI** 
- **Uvicorn** 
- **Beanie**
- **aiohttp** 
- **JWT (python-jose)** 
- **Passlib**
- **Docker + Docker Compose**
- **Nginx** 
- **Redis (async)** - (планируется)
- **pytest** (планиуруется)

## Запуск проекта через docker compose
**Скопироавть проект:**
git clone https://github.com/murzm22/weather_service

**Для работы проекта нужно создать файл .env в корне:**  
*OPENWEATHER_API_KEY=your_openweather_api_key*  
*SECRET_KEY==your_secret_key*  
*MONGO_URL="mongodb://root:example@mongo:27017/weather_service?authSource=admin"*  
*ALGORITHM="HS256"*  

**Сборка из корня проекта:**
docker-compose up --build

**Проверь работу:**
https://localhost/docs

