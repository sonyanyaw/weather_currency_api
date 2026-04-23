import { useEffect, useState } from "react";
import { useWeather } from "./hooks/useWeather";
import { useCurrency } from "./hooks/useCurrency";
import { WeatherCard } from "./components/WeatherCard";
import { CurrencyCard } from "./components/CurrencyCard";

import "./App.css";

export default function App() {
  const { weather, loading: wLoading, error: wError, search } = useWeather();
  const { conversion, loading: cLoading, error: cError, convert } = useCurrency();
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  return (
    <>
      <div className="orb" style={{ width: 360, height: 360, background: "rgba(45,106,223,0.13)", top: -80, left: -80 }} />
      <div className="orb" style={{ width: 260, height: 260, background: "rgba(126,184,247,0.07)", bottom: 0, right: 60, animationDelay: "3s" }} />

      <div style={{ position: "relative", zIndex: 1, maxWidth: 750, width: "100%", margin: "0 auto", padding: "20px 12px 48px" }}>

        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 28 }}>
          <div>
            <div style={{ fontSize: "0.68rem", letterSpacing: "0.18em", color: "#5580a8", textTransform: "uppercase", marginBottom: 5 }}>Live Dashboard</div>
            <h1 style={{ fontSize: "clamp(1.4rem, 5vw, 2.1rem)", fontWeight: 800, color: "#e8f2ff", lineHeight: 1.1 }}>
              Weather &amp; Currency
            </h1>
          </div>
          <div style={{ textAlign: "right", flexShrink: 0 }}>
            <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: "clamp(0.95rem, 3vw, 1.15rem)", color: "#7eb8f7", fontWeight: 500 }}>
              {time.toLocaleTimeString()}
            </div>
            <div style={{ fontSize: "0.72rem", color: "#4a6882", marginTop: 2 }}>
              {time.toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" })}
            </div>
          </div>
        </div>

        <WeatherCard  weather={weather} loading={wLoading} error={wError} onSearch={search} />
        <CurrencyCard conversion={conversion} loading={cLoading} error={cError} onConvert={convert} />

        <div style={{ textAlign: "center", marginTop: 28, color: "#2a3a4e", fontSize: "0.7rem", letterSpacing: "0.05em" }}>
          Powered by Meteosource &amp; ExchangeRate APIs
        </div>
      </div>
    </>
  );
}