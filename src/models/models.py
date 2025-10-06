from pydantic import BaseModel, Field
import decimal

class WeatherResponse(BaseModel):
    city: str
    temperature_c_now: float
    description: str
    temperature_c_today: str
    temperature_c_tomorrow: str

class CurrencyConvertRequest(BaseModel):
    from_currency: str = Field(pattern='^[A-Za-z]{3}$', example="USD", description="Currency code")
    to_currency: str = Field(pattern='^[A-Za-z]{3}$', example="RUB", description="Currency code")
    amount: float = Field(gt=0, example="100", description="Amount must be greater than 0")

class CurrencyConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: decimal.Decimal
    converted_amount: float