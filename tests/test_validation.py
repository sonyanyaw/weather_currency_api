import pytest
import httpx
from decimal import Decimal

from src.services.weather_service import get_weather
from src.services.currency_service import convert_currency


# =========================
# WEATHER TESTS
# =========================

def weather_success_handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={
        "current": {
            "temperature": 18,
            "summary": "Rainy",
            "icon_num": 1,
            "wind": {"speed": 5, "dir": "N"},
            "cloud_cover": 50,
            "precipitation": {"total": 1, "type": "rain"}
        },
        "daily": {
            "data": [
                {
                    "summary": "Today",
                    "all_day": {
                        "temperature_min": 10,
                        "temperature_max": 20
                    }
                },
                {
                    "summary": "Tomorrow",
                    "all_day": {
                        "temperature_min": 12,
                        "temperature_max": 22
                    }
                }
            ]
        },
        "hourly": {
            "data": [
                {
                    "date": "2024-01-01T10:00:00",
                    "temperature": 18,
                    "summary": "Rainy",
                    "icon": 1,
                    "precipitation": {"total": 0.5}
                }
            ]
        }
    })


@pytest.mark.asyncio
async def test_get_weather_success():
    transport = httpx.MockTransport(weather_success_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        result = await get_weather("berlin", client)

    assert result["city"] == "berlin"
    assert result["temperature"] == 18
    assert result["description"] == "Rainy"
    assert result["temp_min"] == 10
    assert result["temp_max"] == 20
    assert isinstance(result["hourly"], list)


@pytest.mark.asyncio
async def test_get_weather_api_error():
    def handler(request):
        return httpx.Response(500, json={})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ValueError):
            await get_weather("berlin", client)


@pytest.mark.asyncio
async def test_get_weather_invalid_data():
    def handler(request):
        return httpx.Response(200, json={"invalid": "data"})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ValueError):
            await get_weather("singapore", client)


# =========================
# CURRENCY TESTS
# =========================

def currency_success_handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={
        "conversion_rates": {
            "USD": 1,
            "EUR": 0.85,
            "GBP": 0.75
        }
    })


@pytest.mark.asyncio
async def test_convert_currency_success():
    transport = httpx.MockTransport(currency_success_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        result = await convert_currency("USD", "EUR", Decimal("100"), client)

    assert result["converted"] == Decimal("85")
    assert result["rate"] == Decimal("0.85")


@pytest.mark.asyncio
async def test_convert_currency_missing_currency():
    def handler(request):
        return httpx.Response(200, json={"conversion_rates": {"USD": 1}})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ValueError):
            await convert_currency("USD", "EUR", Decimal("100"), client)


@pytest.mark.asyncio
async def test_convert_currency_api_error():
    def handler(request):
        return httpx.Response(403, json={})

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(ValueError):
            await convert_currency("USD", "TWD", Decimal("100"), client)


@pytest.mark.asyncio
async def test_convert_currency_same_currency():
    transport = httpx.MockTransport(currency_success_handler)

    async with httpx.AsyncClient(transport=transport) as client:
        result = await convert_currency("USD", "USD", Decimal("100"), client)

    assert result["converted"] == Decimal("100")


# =========================
# INTEGRATION TEST
# =========================

@pytest.mark.asyncio
async def test_multiple_requests_same_client():
    def handler(request: httpx.Request):
        if "meteosource" in request.url.host:
            return weather_success_handler(request)
        return currency_success_handler(request)

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        weather = await get_weather("madrid", client)
        currency = await convert_currency("USD", "EUR", Decimal("50"), client)

    assert weather["city"] == "madrid"
    assert currency["converted"] == Decimal("42.5")