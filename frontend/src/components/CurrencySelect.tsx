import { useState, useRef, useEffect } from "react";

interface Props {
  value: string;
  currencies: string[];
  onChange: (c: string) => void;
}

export function CurrencySelect({ value, currencies, onChange }: Props) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <div ref={ref} style={{ position: "relative", minWidth: 0, flex: 1 }}>
      <button
        onClick={() => setOpen((o) => !o)}
        style={{
          width: "100%", padding: "11px 28px 11px 12px",
          background: "rgba(255,255,255,0.05)",
          border: `1px solid rgba(126,184,247,${open ? 0.6 : 0.2})`,
          borderRadius: 12, color: "#e0eaf8",
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: "0.95rem", fontWeight: 500,
          cursor: "pointer", textAlign: "left",
          transition: "border-color 0.2s", position: "relative",
        }}
      >
        {value}
        <span style={{
          position: "absolute", right: 11, top: "50%",
          transform: `translateY(-50%) rotate(${open ? 180 : 0}deg)`,
          transition: "transform 0.2s", fontSize: "0.55rem", color: "#7eb8f7",
        }}>▼</span>
      </button>

      {open && (
        <div style={{
          position: "absolute", top: "calc(100% + 6px)", left: 0, right: 0,
          background: "#0f1c2e", border: "1px solid rgba(126,184,247,0.2)",
          borderRadius: 12, zIndex: 100,
          boxShadow: "0 12px 40px rgba(0,0,0,0.5)",
          animation: "fadeUp 0.15s ease both",
          maxHeight: 220, overflowY: "auto",
        }}>
          {currencies.map((c) => (
            <div
              key={c}
              onClick={() => { onChange(c); setOpen(false); }}
              style={{
                padding: "10px 14px",
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: "0.85rem",
                color: c === value ? "#7eb8f7" : "#a0bde0",
                background: c === value ? "rgba(126,184,247,0.1)" : "transparent",
                cursor: "pointer",
                transition: "background 0.1s",
                borderLeft: c === value ? "2px solid #7eb8f7" : "2px solid transparent",
              }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLDivElement).style.background = "rgba(126,184,247,0.07)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLDivElement).style.background =
                  c === value ? "rgba(126,184,247,0.1)" : "transparent";
              }}
            >
              {c}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}