# Weather + Currency API

Мини API для получения погоды и конвертации валют.

## Технологии
- Python 3.12
- FastAPI
- httpx
- Pydantic
- dotenv

## Запуск
1. Скопировать `.env.example` → `.env` и добавить ключ OpenWeather.
2. Установить зависимости:
pip install -r requirements.txt
3. Запустить сервер:
uvicorn src.main:app --reload

## Эндпоинты
- GET /weather?city=<город>
- POST /convert

## Примеры запросов
Использовать curl / Postman / Swagger UI

