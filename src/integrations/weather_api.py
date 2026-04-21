import httpx
from src.core.config import settings


async def fetch_weather(city: str, client: httpx.AsyncClient):
    url = (
        f"{settings.weather_base_url}"
        f"?place_id={city}&sections=all&timezone=UTC&language=en&units=metric"
        f"&key={settings.weather_api_key}"
    )

    r = await client.get(url, timeout=10)
    r.raise_for_status()
    return r.json()