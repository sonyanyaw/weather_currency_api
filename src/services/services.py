import os
from typing import Optional
import httpx
from src.utils.utils import get_cache, set_cache

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CURRENCYRATE_API_KEY = os.getenv("CURRENCYRATE_API_KEY")
CACHE_TTL_WEATHER = int(os.getenv("CACHE_TTL_WEATHER", 1800))
CACHE_TTL_CURRENCY = int(os.getenv("CACHE_TTL_CURRENCY", 3600))

async def get_weather(city: str, client: Optional[httpx.AsyncClient] = None):
    if client is None:
        async with httpx.AsyncClient() as client:
            return await get_weather(city, client)
    else:
        key = f"weather:{city.lower()}"
        cached = await get_cache(key)
        if cached:
            return cached

        url = f"https://www.meteosource.com/api/v1/free/point?place_id={city}&sections=all&timezone=UTC&language=en&units=metric&key={WEATHER_API_KEY}"
        # async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        result = {
            "city": city,
            "temperature_c_now": data["current"]["temperature"],
            "description": data["current"]["summary"],
            "temperature_c_today": data["daily"]["data"][0]["summary"],
            "temperature_c_tomorrow": data["daily"]["data"][1]["summary"]
        }
        await set_cache(key, result, CACHE_TTL_WEATHER)
        return result
        
    

async def convert_currency(from_currency: str, to_currency: str, amount: float, client: Optional[httpx.AsyncClient] = None):
    if client is None:
        async with httpx.AsyncClient() as client:
            return await convert_currency(from_currency, to_currency, amount, client)
    else:
        key = f"currency:{from_currency.upper()}_{to_currency.upper()}"
        cached = await get_cache(key)
        if cached:
            rate = cached["rate"]
        else:
            url = f"https://v6.exchangerate-api.com/v6/{CURRENCYRATE_API_KEY}/latest/{from_currency}"
            r = await client.get(url)
            data = r.json()
            rate = data['conversion_rates'][to_currency]
            await set_cache(key, {"rate": rate}, CACHE_TTL_CURRENCY)
        return amount * rate