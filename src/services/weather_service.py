import httpx
from src.core.config import settings
from src.utils.utils import get_cache, set_cache
from src.integrations.weather_api import fetch_weather


async def get_weather(city: str, client: httpx.AsyncClient):
    key = f"weather:{city.strip().lower()}"

    cached = await get_cache(key)
    if cached:
        return cached

    try:
        data = await fetch_weather(city, client)
    except httpx.HTTPError as e:
        raise ValueError("Weather API error") from e

    if "current" not in data:
        raise ValueError("Invalid weather response")

    result = {
        "city": city,
        
        # Current conditions
        "temperature": data["current"]["temperature"],
        "description": data["current"]["summary"],
        "icon": data["current"]["icon_num"],
        "wind_speed": data["current"]["wind"]["speed"],
        "wind_dir": data["current"]["wind"]["dir"],
        "cloud_cover": data["current"]["cloud_cover"],
        "precipitation": data["current"]["precipitation"]["total"],
        "precip_type": data["current"]["precipitation"]["type"],

        # Today's forecast
        "temp_min": data["daily"]["data"][0]["all_day"]["temperature_min"],
        "temp_max": data["daily"]["data"][0]["all_day"]["temperature_max"],
        "summary_today": data["daily"]["data"][0]["summary"],

        # Tomorrow's forecast
        "summary_tomorrow": data["daily"]["data"][1]["summary"],
        "temp_min_tomorrow": data["daily"]["data"][1]["all_day"]["temperature_min"],
        "temp_max_tomorrow": data["daily"]["data"][1]["all_day"]["temperature_max"],

        # Hourly strip (next 6 hours for a chart)
        "hourly": [
            {
                "time": h["date"][11:16],  
                "temp": h["temperature"],
                "weather": h["summary"],
                "icon": h["icon"],
                "precip": h["precipitation"]["total"],
            }
            for h in data["hourly"]["data"][:6]
        ],
    }

    await set_cache(key, result, settings.cache_ttl_weather)
    return result