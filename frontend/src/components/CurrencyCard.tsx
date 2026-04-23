import { useState } from "react";
import { CurrencySelect } from "./CurrencySelect";
import { Skeleton } from "./Skeleton";
import type { ConversionData } from "../types";
import { CURRENCIES } from "../constants";

interface Props {
  conversion: ConversionData | null;
  loading: boolean;
  error: string | null;
  onConvert: (from: string, to: string, amount: number) => void;
}

export function CurrencyCard({ conversion, loading, error, onConvert }: Props) {
  const [amount, setAmount] = useState("100");
  const [from, setFrom]     = useState("USD");
  const [to, setTo]         = useState("EUR");

  const swap = () => { setFrom(to); setTo(from); };

  const handleConvert = () => {
    const n = parseFloat(amount);
    if (!isNaN(n) && n > 0) onConvert(from, to, n);
  };

  return (
    <div className="card" style={{ padding: "24px" }}>
      <div style={{ fontSize: "0.68rem", letterSpacing: "0.14em", color: "#5580a8", textTransform: "uppercase", marginBottom: 16 }}>
        Currency Converter
      </div>

      {/* Controls */}
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>

    {/* Row 1: amount + from + swap + to */}
    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input
        className="glass-input"
        type="number" min="0"
        style={{ width: 90, flexShrink: 0, padding: "11px 10px", fontFamily: "'JetBrains Mono', monospace", fontSize: "0.95rem" }}
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleConvert()}
        />
        <CurrencySelect value={from} currencies={CURRENCIES} onChange={(c) => setFrom(c)} />
        <button className="swap-btn" onClick={swap} title="Swap" style={{ flexShrink: 0 }}>⇄</button>
        <CurrencySelect value={to} currencies={CURRENCIES} onChange={(c) => setTo(c)} />
    </div>

    {/* Row 2: full-width convert button */}
    <button
        className="btn-primary"
        style={{ width: "100%", padding: "12px", fontSize: "0.95rem" }}
        onClick={handleConvert}
    >
        {loading
        ? <span className="loader" style={{ width: 16, height: 16, borderWidth: 2 }} />
        : "Convert"}
    </button>
    </div>

      {loading && (
        <div style={{ marginTop: 18, display: "flex", gap: 8 }}>
          <Skeleton w="200px" h="2.2rem" />
          <Skeleton w="80px"  h="2.2rem" />
        </div>
      )}

      {error && !loading && (
        <div className="error-box" style={{ marginTop: 14 }}>⚠ {error}</div>
      )}

      {conversion && !loading && (
        <div style={{ marginTop: 18, animation: "fadeUp 0.35s ease both" }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
            <span style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: "clamp(1.5rem, 5vw, 2rem)",
              fontWeight: 500, color: "#7eb8f7",
            }}>
              {Number(conversion.converted_amount).toLocaleString(undefined, { maximumFractionDigits: 4 })}
            </span>
            <span style={{ fontSize: "1rem", color: "#5580a8" }}>{conversion.to_currency}</span>
            <span style={{ fontSize: "0.78rem", color: "#3a5268" }}>
              1 {conversion.from_currency} = {Number(conversion.rate).toFixed(6)} {conversion.to_currency}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}