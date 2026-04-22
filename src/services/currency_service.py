from decimal import Decimal

from src.integrations.currency_api import fetch_rate
from src.core.config import settings
from src.utils.utils import get_cache, set_cache


async def convert_currency(from_currency, to_currency, amount, client):
    key = f"currency:{from_currency}_{to_currency}"

    cached = await get_cache(key)
    if cached:
        rate = Decimal(cached["rate"])
    else:
        rate = await fetch_rate(from_currency, to_currency, client)
        await set_cache(key, {"rate": str(rate)}, settings.cache_ttl_currency)

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted": round(amount * rate, 2),
        "rate": rate,
    }