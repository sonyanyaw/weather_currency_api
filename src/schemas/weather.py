from pydantic import BaseModel
from typing import List

class HourlyEntry(BaseModel):
    time: str
    temp: float
    weather: str
    icon: int
    precip: float

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    icon: int
    wind_speed: float
    wind_dir: str
    cloud_cover: int
    precipitation: float
    precip_type: str
    temp_min: float
    temp_max: float
    summary_today: str
    summary_tomorrow: str
    temp_min_tomorrow: float
    temp_max_tomorrow: float
    hourly: List[HourlyEntry]