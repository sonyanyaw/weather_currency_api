from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    weather_api_key: str = "test"
    currencyrate_api_key: str = "test"

    redis_url: str = "redis://localhost:6379"

    cache_ttl_weather: int = 1800
    cache_ttl_currency: int = 3600

    weather_base_url: str = "https://www.meteosource.com/api/v1/free/point"
    currency_base_url: str = "https://v6.exchangerate-api.com/v6"


    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()