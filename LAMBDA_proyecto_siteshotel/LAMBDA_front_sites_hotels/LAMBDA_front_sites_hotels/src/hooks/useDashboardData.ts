import { useState, useEffect } from "react";
import { apiService } from "@/lib/api";
import { useFilters, DateFilter } from "@/contexts/FilterContext";

export const useDashboardData = () => {
  const { property, area, dateFilter } = useFilters();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        console.log('🔍 Solicitando datos con filtros:', { property, area, dateFilter });
        
        // Enviar filtros jerárquicos directamente al backend
        const response = await apiService.getDashboardMetrics(property, area, dateFilter);
        setData(response.metrics || response);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [property, area, dateFilter]);

  return { data, loading, error };
};
