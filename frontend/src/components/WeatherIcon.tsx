const ICONS: Record<string, string> = {
  "clear": "☀️", "sunny": "☀️",
  "partly sunny": "🌤️", "partly clear": "🌤️",
  "mostly cloudy": "🌥️", "cloudy": "☁️", "overcast": "☁️",
  "light rain": "🌦️", "rain shower": "🌧️", "rain": "🌧️",
  "thunderstorm": "🌩️", "snow": "❄️", "fog": "🌫️", "mist": "🌫️",
};

export function WeatherIcon({ code, size = 64 }: { code?: string; size?: number }) {
  const key = Object.keys(ICONS).find((k) => code?.toLowerCase().includes(k));
  return <span style={{ fontSize: size }}>{key ? ICONS[key] : "🌡️"}</span>;
}