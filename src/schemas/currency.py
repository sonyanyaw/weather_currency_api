from pydantic import BaseModel, Field
from decimal import Decimal


class CurrencyConvertRequest(BaseModel):
    from_currency: str = Field(pattern='^[A-Za-z]{3}$', example="USD", description="Currency code")
    to_currency: str = Field(pattern='^[A-Za-z]{3}$', example="EUR", description="Currency code")
    amount: float = Field(gt=0, example=100, description="Amount must be greater than 0")

class CurrencyConvertResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: Decimal
    converted_amount: Decimal
    rate: Decimal