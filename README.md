# Weather + Currency API

Мини API для получения погоды для заданного города и конвертации валют.
Поддерживает кэширование через Redis и интеграцию с Telegram-ботом.

## Технологии

- Python 3.12
- FastAPI
- uvicorn
- httpx
- Pydantic
- python-dotenv  
- Redis (для кэширования)  
- pytest
- pytest-asyncio
- redis
- aiogram
- Docker / docker-compose  

---

## Быстрый запуск

### Локально

1. Скопировать `.env.example` → `.env` и добавить свои ключи:
   ```text
   WEATHER_API_KEY=ваш_ключ
   CURRENCYRATE_API_KEY=ваш_ключ
   REDIS_URL=redis://localhost:6379/0
   CACHE_TTL_WEATHER=600
   CACHE_TTL_CURRENCY=3600
   TELEGRAM_BOT_TOKEN=токен_телеграм_бота

2. Установить зависимости:
pip install -r requirements.txt

3. Запустить сервер:
uvicorn src.main:app --reload

4. Swagger UI:
http://127.0.0.1:8000/docs


### Через Docker

1. Скопировать .env.example → .env
2. Запустить контейнеры:
docker-compose up --build

3. API доступно:
http://localhost:8000

4. Swagger UI:
http://localhost:8000/docs

---

## Эндпоинты
### GET /weather?city=<город>

Пример запроса:
GET /weather?city=Taipei

Пример ответа:
{
  "city": "Taipei",
  "temperature_c_now": 26.0,
  "description": "clear sky",
  "temperature_c_today": "Sunny. Temperature 20/30 °C.",
  "temperature_c_now": "Cloudy. Temperature 17/27 °C.",
}

### POST /convert
Конвертация валюты по текущему курсу.

Тело запроса:
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 100
}

Пример ответа:
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 100,
  "converted_amount": 92.5
}

---

## Особенности реализации и доработок

- Асинхронные запросы к внешним API (httpx)
- Кэширование через Redis (fire-and-forget подход для записи, таймауты)
- Настраиваемый TTL для кэша через .env
- Логирование ошибок и таймаутов кэша
- Контейнеризация через Docker + docker-compose
- Поддержка Telegram-бота через aiogram

---

## Структура проекта

weather_currency_api/
├─ src/
│   ├─ main.py           # Точка входа FastAPI
│   ├─ models/
│   │   ├─ models.py         # Pydantic модели для валидации
│   ├─ routes/
│   │   ├─ routes.py         # Эндпоинты
│   ├─ services/
│   │   ├─ services.py       # Логика погоды и конвертации
│   ├─ services/
│   │   ├─ utils.py          # Кэширование, Redis helper
│   └─ bot.py            # Telegram-бот
├─ tests/                # Тесты
│   └─ test_validation.py  
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .env.example
└─ README.md

---

## Тестирование

### Локально:

pytest -q

### В Docker:

docker-compose exec web pytest -q
