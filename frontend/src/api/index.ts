import { BASE } from "../constants";
import type { WeatherData, ConversionData } from "../types";

export async function fetchWeather(city: string): Promise<WeatherData> {
  const res = await fetch(`${BASE}/weather?city=${encodeURIComponent(city)}`);
  if (!res.ok) throw new Error((await res.json()).detail || "City not found");
  return res.json();
}

export async function fetchCurrency(
  from: string, to: string, amount: number
): Promise<ConversionData> {
  const res = await fetch(`${BASE}/currency?from_cur=${from}&to=${to}&amount=${amount}`);
  if (!res.ok) throw new Error((await res.json()).detail || "Conversion failed");
  return res.json();
}