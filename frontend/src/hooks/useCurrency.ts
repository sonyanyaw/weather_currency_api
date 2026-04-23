import { useState } from "react";
import { fetchCurrency } from "../api";
import type { ConversionData } from "../types";

export function useCurrency() {
  const [conversion, setConversion] = useState<ConversionData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const convert = async (from: string, to: string, amount: number) => {
    if (!amount || isNaN(amount)) return;
    setLoading(true);
    setError(null);
    setConversion(null);
    try {
      const data = await fetchCurrency(from, to, amount);
      setConversion(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return { conversion, loading, error, convert };
}