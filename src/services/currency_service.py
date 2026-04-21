import httpx
from src.core.config import settings
from src.utils.utils import get_cache, set_cache


async def convert_currency(
    from_currency: str,
    to_currency: str,
    amount: float,
    client: httpx.AsyncClient,
):
    key = f"currency:{from_currency.upper()}_{to_currency.upper()}"

    cached = await get_cache(key)
    if cached:
        rate = cached["rate"]
    else:
        url = (
            f"{settings.currency_base_url}/"
            f"{settings.currencyrate_api_key}/latest/{from_currency}"
        )

        r = await client.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        rates = data.get("conversion_rates", {})
        rate = rates.get(to_currency)

        if rate is None:
            raise ValueError(f"Currency {to_currency} not found")

        await set_cache(key, {"rate": rate}, settings.cache_ttl_currency)

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted": amount * rate,
        "rate": rate,
    }