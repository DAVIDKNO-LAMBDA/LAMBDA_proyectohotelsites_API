/**
 * Dashboard Power BI - Réplica exacta del dashboard de Power BI
 * 
 * Esta página replica exactamente la estructura y métricas del Power BI
 * para evitar confusiones y trabajar con una réplica exacta.
 */

import React from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useFilters } from "@/contexts/FilterContext";
import { KPICard } from "@/components/dashboard/KPICard";
import { useDashboardData } from "@/hooks/useDashboardData";

export const DashboardPowerBI: React.FC = () => {
  // Obtener información del usuario
  const { user } = useAuth();
  const { property, area, dateFilter } = useFilters();

  // Datos reales desde backend
  const { data: kpiData, loading, error } = useDashboardData();

  if (loading) return <div className="text-center text-muted-foreground">Cargando métricas...</div>;
  if (error) return <div className="text-center text-destructive">Error: {error}</div>;
  if (!kpiData) return <div className="text-center text-muted-foreground">Sin datos disponibles</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Dashboard Administrativo</h1>
          <p className="text-muted-foreground">
            Información detallada de operaciones y rendimiento - Todas las áreas
          </p>
        </div>
      </div>

      {/* === FILA 1: MÉTRICAS PRINCIPALES === */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard
          title="% Ocupación"
          value={`${kpiData["%ocupacion"].toFixed(2)}%`}
          subtitle="Tasa promedio de ocupación"
          trend={kpiData["%cumplimiento_ocup"] >= 100 ? "positive" : "negative"}
          trendValue={`${kpiData["%cumplimiento_ocup"].toFixed(2)}%`}
        />

        <KPICard
          title="Ventas"
          value={`$${kpiData["ventas_totales"].toLocaleString()}`}
          subtitle="Revenue total"
          trend="neutral"
          trendValue=""
        />

        <KPICard
          title="ADR"
          value={`$${kpiData["adr"].toLocaleString()}`}
          subtitle=""
          trend={kpiData["%cumplimiento_adr"] >= 100 ? "positive" : "negative"}
          trendValue={`${kpiData["%cumplimiento_adr"].toFixed(2)}%`}
        />

        <KPICard
          title="RevPAR"
          value={`$${kpiData["revpar"].toLocaleString()}`}
          subtitle=""
          trend="neutral"
          trendValue=""
        />
      </div>

      {/* === FILA 2: PRESUPUESTOS === */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard
          title="Presupuesto % ocupación"
          value={`${kpiData["%ocupacion_ppto"].toFixed(0)}%`}
          subtitle="Tasa promedio presupuestada"
          trend="neutral"
          trendValue=""
        />

        <KPICard
          title="Presupuesto a hoy"
          value={`$${kpiData["ppto_hoy"].toLocaleString()}`}
          subtitle="Alojamiento"
          trend="positive"
          trendValue="112.24%"
        />

        <KPICard
          title="ADR"
          value={`$${kpiData["adr_ppto"].toLocaleString()}`}
          subtitle="Presupuesto"
          trend="neutral"
          trendValue=""
        />

        <KPICard
          title="RevPAR (Forecast)"
          value={`$${kpiData["revpar_forecast"].toLocaleString()}`}
          subtitle=""
          trend="neutral"
          trendValue=""
        />
      </div>

      {/* === FILA 3: PRESUPUESTOS ADICIONALES === */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard
          title="Presupuesto % ocupación"
          value={`${kpiData["%ocupacion_ppto"].toFixed(0)}%`}
          subtitle="Tasa promedio presupuestada"
          trend="neutral"
          trendValue=""
        />

        <KPICard
          title="Presupuesto de ventas"
          value={`${kpiData["forecast_ventas"].toLocaleString()}`}
          subtitle="Alojamiento"
          trend="positive"
          trendValue="112.24%"
        />

        <KPICard
          title="ADR Forecast"
          value={`$${kpiData["adr_forecast"].toLocaleString()}`}
          subtitle="Presupuesto"
          trend="neutral"
          trendValue=""
        />

        <KPICard
          title="Tarifa promedio (Per)"
          value={`$${kpiData["tarifa_per"].toLocaleString()}`}
          subtitle="Tarifa promedio por persona"
          trend="neutral"
          trendValue=""
        />
      </div>

      {/* === FILA 4: FORECAST Y OTROS === */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPICard
          title="Gastos y costos"
          value={`$${kpiData["gastos_costos"].toLocaleString()}`}
          subtitle=""
          trend="neutral"
          trendValue=""
        />

        <KPICard
          title="Forecast de ventas"
          value={`${kpiData["forecast_ventas"].toLocaleString()}`}
          subtitle="Alojamiento"
          trend="neutral"
          trendValue=""
        />

        <KPICard
          title="Utilidad/Pérdida"
          value={`$${kpiData["utilidad"].toLocaleString()}`}
          subtitle="Resultado operativo (GOP)"
          trend={kpiData["utilidad"] > 0 ? "positive" : "negative"}
          trendValue={`${kpiData["%gop"].toFixed(2)}%`}
        />

        <KPICard
          title="FARA"
          value={`$${kpiData["fara"].toLocaleString()}`}
          subtitle="Factor de administración y reserva"
          trend="neutral"
          trendValue="7%"
        />
      </div>
    </div>
  );
};

export default DashboardPowerBI;