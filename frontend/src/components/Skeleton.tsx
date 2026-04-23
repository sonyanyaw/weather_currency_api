export function Skeleton({ w = "100%", h = "1rem", radius = "6px" }: {
  w?: string; h?: string; radius?: string;
}) {
  return (
    <div style={{
      width: w, height: h, borderRadius: radius,
      background: "linear-gradient(90deg,#1e2a3a 25%,#263445 50%,#1e2a3a 75%)",
      backgroundSize: "400% 100%",
      animation: "shimmer 1.6s infinite",
    }} />
  );
}