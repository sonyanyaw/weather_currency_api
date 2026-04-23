export const BASE = import.meta.env.PROD
  ? "https://your-app.vercel.app"
  : "http://localhost:8000";

export const QUICK_CITIES = [
  "Moscow", "London", "Shanghai", "Tokyo",
  "Seoul", "Taipei", "Sydney", "Paris", "Dubai", "Toronto",
];

export const CURRENCIES = [
  "USD", "EUR", "RUB", "TWD", "GBP", "JPY",
  "AUD", "CAD", "CHF", "CNY", "SGD", "AED", "INR", "BRL",
];