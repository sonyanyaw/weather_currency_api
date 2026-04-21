from fastapi import APIRouter, Depends, HTTPException
import httpx

from src.routes.deps import get_http_client
from src.services.weather_service import get_weather
from src.services.currency_service import convert_currency
from src.schemas.weather import WeatherResponse
from src.schemas.currency import CurrencyConvertResponse

router = APIRouter()


@router.get("/weather", response_model=WeatherResponse)
async def weather(
    city: str,
    client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        return await get_weather(city, client)

    except ValueError:
        raise HTTPException(status_code=404, detail="City not found")

    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="External weather service error")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/currency", response_model=CurrencyConvertResponse)
async def convert(
    from_cur: str,
    to: str,
    amount: float,
    client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        result = await convert_currency(from_cur.upper(), to.upper(), amount, client)

        print(result)

        return CurrencyConvertResponse(
            from_currency=from_cur.upper(),
            to_currency=to.upper(),
            amount=amount,
            converted_amount=result["converted"],
            rate=result["rate"],
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="External currency service error")

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")