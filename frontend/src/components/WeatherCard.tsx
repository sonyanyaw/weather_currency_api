import type { WeatherData } from "../types";
import { WeatherIcon } from "./WeatherIcon";
import { Skeleton } from "./Skeleton";
import { QUICK_CITIES } from "../constants";
import { useRef, useState } from "react";

const tempColor = (t: number | null) => {
  if (t == null) return "#7eb8f7";
  if (t <= 0)  return "#89d4f5";
  if (t <= 15) return "#7eb8f7";
  if (t <= 25) return "#f7c97e";
  return "#f7897e";
};

interface Props {
  weather: WeatherData | null;
  loading: boolean;
  error: string | null;
  onSearch: (city: string) => void;
}

export function WeatherCard({ weather, loading, error, onSearch }: Props) {
  const [city, setCity] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSearch = (q = city) => {
    if (!q.trim()) return;
    setCity(q);
    onSearch(q);
  };

  return (
    <div className="card" style={{ padding: "24px", marginBottom: 16 }}>

      {/* Search */}
      <div style={{ display: "flex", gap: 8, marginBottom: 14 }}>
        <input
          ref={inputRef}
          className="glass-input"
          style={{ flex: 1, minWidth: 0, padding: "11px 14px", fontSize: "0.9rem" }}
          placeholder="Search a city…"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button
          className="btn-primary"
          style={{ padding: "11px 18px", fontSize: "0.9rem" }}
          onClick={() => handleSearch()}
        >
          {loading
            ? <span className="loader" style={{ width: 16, height: 16, borderWidth: 2 }} />
            : "Search"}
        </button>
      </div>

      {/* Quick cities — horizontal scroll on mobile */}
      <div style={{
        display: "flex", gap: 7, overflowX: "auto", paddingBottom: 4,
        scrollbarWidth: "none", marginBottom: weather || loading || error ? 20 : 0,
      }}>
        {QUICK_CITIES.map((c) => (
          <button key={c} className="quick-city" onClick={() => handleSearch(c)}>{c}</button>
        ))}
      </div>

      {/* Skeleton */}
      {loading && (
        <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
          <Skeleton w="68px" h="68px" radius="50%" />
          <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 8 }}>
            <Skeleton w="50%" h="2rem" />
            <Skeleton w="30%" h="0.9rem" />
            <div style={{ display: "flex", gap: 8, marginTop: 4, flexWrap: "wrap" }}>
              {[1,2,3,4].map((i) => <Skeleton key={i} w="76px" h="58px" radius="10px" />)}
            </div>
          </div>
        </div>
      )}

      {/* Error */}
      {error && !loading && (
        <div className="error-box">⚠ {error}</div>
      )}

      {/* Result */}
      {weather && !loading && (
        <div style={{ animation: "fadeUp 0.4s ease both" }}>

          {/* Temp row */}
          <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 16, flexWrap: "wrap" }}>
            <WeatherIcon code={weather.description} size={60} />
            <div>
              <div style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: "clamp(2rem, 8vw, 3.2rem)",
                fontWeight: 500,
                color: tempColor(weather.temperature),
                lineHeight: 1,
              }}>
                {Math.round(weather.temperature)}°C
              </div>
              <div style={{ color: "#7eb8f7", fontSize: "0.95rem", marginTop: 3, textTransform: "capitalize" }}>
                {weather.description}
              </div>
              <div style={{ color: "#4a6882", fontSize: "0.78rem", marginTop: 1 }}>
                {weather.city}
              </div>
            </div>
          </div>

          {/* Pills — wrap naturally on mobile */}
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 16 }}>
            {[
              { label: "Today's range", value: `${Math.round(weather.temp_min)}–${Math.round(weather.temp_max)}°C`, icon: "📅" },
              { label: "Wind",          value: `${Math.round(weather.wind_speed)} m/s ${weather.wind_dir}`, icon: "🌬" },
              { label: "Cloud cover",   value: `${weather.cloud_cover}%`, icon: "☁️" },
              { label: "Precipitation", value: `${weather.precipitation} mm`, icon: "💧" },
            ].map(({ label, value, icon }) => (
              <div key={label} className="stat-pill" style={{ flex: "1 1 calc(50% - 4px)", minWidth: 110 }}>
                <span style={{ fontSize: "1rem" }}>{icon}</span>
                <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: "0.88rem", color: "#c8dff5", fontWeight: 500 }}>{value}</span>
                <span style={{ fontSize: "0.65rem", color: "#4a6882", textTransform: "uppercase", letterSpacing: "0.06em" }}>{label}</span>
              </div>
            ))}
          </div>

          {/* Summaries */}
          {weather.summary_today && (
            <div style={{ fontSize: "0.8rem", color: "#5580a8", borderTop: "1px solid rgba(126,184,247,0.08)", paddingTop: 12 }}>
              <span style={{ color: "#7eb8f7" }}>Today · </span>{weather.summary_today}
            </div>
          )}
          {weather.summary_tomorrow && (
            <div style={{ marginTop: 5, fontSize: "0.8rem", color: "#5580a8" }}>
              <span style={{ color: "#7eb8f7" }}>Tomorrow · </span>{weather.summary_tomorrow}
            </div>
          )}
        </div>
      )}
    </div>
  );
}