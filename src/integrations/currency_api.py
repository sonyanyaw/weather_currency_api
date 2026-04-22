import httpx
from decimal import Decimal

from src.core.config import settings


async def fetch_rate(from_currency: str, to_currency: str, client: httpx.AsyncClient):
    url = f"{settings.currency_base_url}/{settings.currencyrate_api_key}/latest/{from_currency}"

    try:
        r = await client.get(url, timeout=10)
        r.raise_for_status()
    except httpx.HTTPError as e:
        raise ValueError("Currency API error") from e

    data = r.json()

    rate = data.get("conversion_rates", {}).get(to_currency)
    
    if rate is None:
        raise ValueError("Currency not found")

    return Decimal(str(rate))