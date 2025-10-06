from fastapi import APIRouter, HTTPException
from src.models.models import WeatherResponse, CurrencyConvertRequest, CurrencyConvertResponse
from src.services.services import get_weather, convert_currency

router = APIRouter()

@router.get("/weather", response_model=WeatherResponse)
async def weather(city: str):
    try:
        return await get_weather(city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail="City not found")
    except Exception:
        raise HTTPException(status_code=502, detail="External weather service error")
    
@router.post("/convert", response_model=CurrencyConvertResponse)
async def convert(request: CurrencyConvertRequest):
    try:
        converted = await convert_currency(request.from_currency.upper(), request.to_currency.upper(), request.amount)
        return CurrencyConvertResponse(
            from_currency=request.from_currency.upper(),
            to_currency=request.to_currency.upper(),
            amount=request.amount,
            converted_amount=converted
        )
    except KeyError:
        raise HTTPException(status_code=400, detail="Conversion data unavailable")
    except Exception:
        raise HTTPException(status_code=502, detail="External currency service error")