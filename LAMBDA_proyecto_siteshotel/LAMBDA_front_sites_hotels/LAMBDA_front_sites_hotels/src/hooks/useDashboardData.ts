import { useState, useEffect } from "react";
import { apiService } from "@/lib/api";

export const useDashboardData = (property: string, area: string, period: string) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!property) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await apiService.getDashboardMetrics(property, area, period);
        setData(response.metrics || response);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [property, area, period]);

  return { data, loading, error };
};
