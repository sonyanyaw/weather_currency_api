export interface HourlyEntry {
  time: string;
  temp: number;
  weather: string;
  icon: number;
  precip: number;
}

export interface WeatherData {
  city: string;
  temperature: number;
  description: string;
  icon: number;
  wind_speed: number;
  wind_dir: string;
  cloud_cover: number;
  precipitation: number;
  precip_type: string;
  temp_min: number;
  temp_max: number;
  summary_today: string;
  summary_tomorrow: string;
  temp_min_tomorrow: number;
  temp_max_tomorrow: number;
  hourly: HourlyEntry[];
}

export interface ConversionData {
  from_currency: string;
  to_currency: string;
  amount: number;
  converted_amount: number;
  rate: number;
}