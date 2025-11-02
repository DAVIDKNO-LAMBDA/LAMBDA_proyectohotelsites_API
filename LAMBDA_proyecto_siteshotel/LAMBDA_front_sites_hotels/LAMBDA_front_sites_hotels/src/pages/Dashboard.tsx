/**
 * Dashboard - Página Principal del Dashboard
 * 
 * Esta es la vista principal que ven los usuarios al iniciar sesión.
 * Muestra diferentes KPIs y visualizaciones según el rol del usuario:
 * 
 * - INVERSIONISTA: Ve KPIs de alto nivel (ROI, ganancias netas, ocupación promedio)
 * - ADMINISTRADOR: Ve KPIs operativos detallados y gráficos de tendencias
 * 
 * Los datos se filtran según la propiedad y el periodo seleccionados
 * en el FilterContext
 */

import React from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useFilters } from "@/contexts/FilterContext";
import { KPICard } from "@/components/dashboard/KPICard";
import { LineChart } from "@/components/dashboard/LineChart";
import { BarChart } from "@/components/dashboard/BarChart";
import { PieChart } from "@/components/dashboard/PieChart";
import { useDashboardData } from "@/hooks/useDashboardData";

// 👇 deja esto SOLO por ahora (solo los gráficos usan dummyData)
import {
  formatCurrency,
  formatPercentage,
  salesTrendData,
  occupancyTrendData,
  avgRateTrendData,
  revPARTrendData,
  propertyRatingsData,
  propertyDistributionData,
} from "@/lib/dummyData";
/**
 * Componente Dashboard Principal
 */
export const Dashboard: React.FC = () => {
  // Obtener información del usuario y filtros
  const { user } = useAuth();
  const { property, area, period } = useFilters();

  // Obtener datos de KPIs según la propiedad seleccionada
  //const kpiData = getKPIData(property);

  // Datos reales desde backend
const { data: kpiData, loading, error } = useDashboardData(property, area, period);

if (loading) return <div className="text-center text-muted-foreground">Cargando métricas...</div>;
if (error) return <div className="text-center text-destructive">Error: {error}</div>;
if (!kpiData) return <div className="text-center text-muted-foreground">Sin datos disponibles</div>;


  /**
   * Vista del Dashboard para INVERSIONISTAS
   * Muestra solo los KPIs más importantes a alto nivel
   */
  if (user?.role === 'Inversionista') {
    return (
      <div className="space-y-6">
        {/* Título y descripción */}
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard de Inversionista</h1>
          <p className="text-muted-foreground mt-1">
            Vista general de rendimiento y métricas clave
          </p>
        </div>

        {/* Grid de KPIs principales - 4 columnas en desktop */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* KPI: RevPAR (Revenue Per Available Room) */}
          <KPICard
            title="RevPAR"
            value={formatCurrency(kpiData.revPAR)}
            subtitle="Ingreso por habitación disponible"
            trend="positive"
            trendValue={formatPercentage(19.9)}
          />

          {/* KPI: Ganancia Neta */}
          <KPICard
            title="Ganancia Neta"
            value={formatCurrency(kpiData.profitMargin)}
            subtitle={`${formatPercentage(kpiData.profitPercentage)} de margen`}
            trend="positive"
            trendValue={formatPercentage(45.5)}
          />

          {/* KPI: Ocupación Promedio */}
          <KPICard
            title="Ocupación Promedio"
            value={formatPercentage(kpiData.avgOccupancyRate)}
            subtitle="Tasa promedio del periodo"
            trend={kpiData.avgOccupancyRate > kpiData.budgetOccupancyRate ? 'positive' : 'negative'}
            trendValue={formatPercentage(Math.abs(kpiData.avgOccupancyRate - kpiData.budgetOccupancyRate))}
          />

          {/* KPI: Ventas Totales */}
          <KPICard
            title="Ventas Totales"
            value={formatCurrency(kpiData.totalRevenue)}
            subtitle={`${formatPercentage(kpiData.revenueAchievement)} vs presupuesto`}
            trend="positive"
            trendValue={formatPercentage(kpiData.revenueAchievement)}
          />
        </div>

        {/* Gráficos de tendencias - 2 columnas */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Gráfico de tendencia de ingresos (RevPAR) */}
          <LineChart
            title="Tendencia de RevPAR"
            data={revPARTrendData}
            dataKeys={[
              { key: 'value', label: 'Actual', color: 'hsl(var(--chart-1))' },
              { key: 'forecast', label: 'Forecast', color: 'hsl(var(--chart-4))' },
            ]}
            formatValue={(value) => formatCurrency(value)}
          />

          {/* Gráfico de distribución por propiedad */}
          <PieChart
            title="Distribución por Propiedad"
            data={propertyDistributionData}
            dataKey="value"
            nameKey="name"
            showPercentage={true}
          />
        </div>
      </div>
    );
  }

  /**
   * Vista del Dashboard para ADMINISTRADORES
   * Muestra KPIs detallados y múltiples gráficos operativos
   */
  return (
    <div className="space-y-6">
      {/* Título y descripción */}
      <div>
        <h1 className="text-3xl font-bold text-foreground">Dashboard Administrativo</h1>
        <p className="text-muted-foreground mt-1">
          Información detallada de operaciones y rendimiento
        </p>
      </div>

     {/* === KPIs PRINCIPALES === */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  <KPICard
    title="% Ocupación"
    value={`${kpiData["%ocupacion"].toFixed(2)}%`}
    subtitle="Tasa promedio de ocupación"
    trend={kpiData["%cumplimiento_ocup"] >= 100 ? "positive" : "negative"}
    trendValue={`${kpiData["%cumplimiento_ocup"].toFixed(2)}%`}
  />

  <KPICard
    title="Ventas"
    value={`$${kpiData["forecast_ventas"].toLocaleString()}`}
    subtitle="Revenue total"
    trend={kpiData["%cumplimiento_ventas"] >= 100 ? "positive" : "negative"}
    trendValue={`${kpiData["%cumplimiento_ventas"].toFixed(2)}%`}
  />

  <KPICard
    title="ADR"
    value={`$${kpiData["adr"].toLocaleString()}`}
    subtitle="Tarifa diaria promedio"
    trend={kpiData["adr_forecast"] > kpiData["adr"] ? "positive" : "negative"}
    trendValue={`$${kpiData["adr_forecast"].toLocaleString()}`}
  />

  <KPICard
    title="RevPAR"
    value={`$${kpiData["revpar"].toLocaleString()}`}
    subtitle="Ingreso por habitación disponible"
    trend={kpiData["revpar_forecast"] > kpiData["revpar"] ? "positive" : "negative"}
    trendValue={`$${kpiData["revpar_forecast"].toLocaleString()}`}
  />
</div>

     {/* === PRESUPUESTO Y FORECAST === */}
<div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
  <KPICard
    title="Presupuesto a hoy"
    value={`$${kpiData["ppto_hoy"].toLocaleString()}`}
    subtitle="Alojamiento"
    trend={kpiData["%cumplimiento_ventas"] >= 100 ? "positive" : "negative"}
    trendValue={`${kpiData["%cumplimiento_ventas"].toFixed(2)}%`}
  />

  <KPICard
    title="Forecast de ventas"
    value={`$${kpiData["forecast_ventas"].toLocaleString()}`}
    subtitle="Alojamiento"
  />

  <KPICard
    title="Tarifa promedio (Per)"
    value={`$${kpiData["tarifa_per"].toLocaleString()}`}
    subtitle="Tarifa promedio por persona"
  />
</div>
{/* === GASTOS, UTILIDAD Y FARA === */}
<div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
  <KPICard
    title="Gastos y costos"
    value={`$${kpiData["gastos_costos"].toLocaleString()}`}
    subtitle="Total de egresos operativos"
  />

  <KPICard
    title="Utilidad / Pérdida"
    value={`$${kpiData["utilidad"].toLocaleString()}`}
    subtitle="Resultado operativo (GOP)"
    trend={kpiData["utilidad"] >= 0 ? "positive" : "negative"}
    trendValue={`${kpiData["%gop"].toFixed(2)}%`}
  />

  <KPICard
    title="FARA"
    value={`$${kpiData["fara"].toLocaleString()}`}
    subtitle="Factor de administración y reserva"
  />
</div>


      {/* Sección de gráficos de tendencias */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-foreground">Tendencias</h2>

        {/* Grid de gráficos - 2 columnas */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Gráfico: Evolución de ventas totales */}
          <LineChart
            title="Total ventas"
            data={salesTrendData}
            dataKeys={[
              { key: 'value', label: 'Leyenda', color: 'hsl(var(--chart-5))' },
              { key: 'forecast', label: 'Presupuesto', color: 'hsl(var(--chart-3))' },
              { key: 'historical', label: 'AGOS', color: 'hsl(var(--chart-1))' },
            ]}
            formatValue={(value) => formatCurrency(value)}
          />

          {/* Gráfico: Evolución de tasa de ocupación */}
          <LineChart
            title="Evolución tasa de ocupación"
            data={occupancyTrendData}
            dataKeys={[
              { key: 'forecast', label: 'Forecast', color: 'hsl(var(--chart-1))' },
              { key: 'value', label: 'ADR', color: 'hsl(var(--chart-2))' },
              { key: 'budget', label: 'Presupuestado', color: 'hsl(var(--chart-5))' },
            ]}
            formatValue={(value) => `${value}%`}
          />

          {/* Gráfico: Evolución de tarifa promedio */}
          <LineChart
            title="Evolución tarifa promedio"
            data={avgRateTrendData}
            dataKeys={[
              { key: 'forecast', label: 'Forecast', color: 'hsl(var(--chart-1))' },
              { key: 'value', label: 'ADR', color: 'hsl(var(--chart-2))' },
              { key: 'budget', label: 'ADR presupuestado', color: 'hsl(var(--chart-5))' },
            ]}
            formatValue={(value) => formatCurrency(value)}
          />

          {/* Gráfico: Evolución de RevPAR */}
          <LineChart
            title="Evolución RevPAR"
            data={revPARTrendData}
            dataKeys={[
              { key: 'forecast', label: 'Forecast', color: 'hsl(var(--chart-1))' },
              { key: 'value', label: 'Actual', color: 'hsl(var(--chart-2))' },
            ]}
            formatValue={(value) => formatCurrency(value)}
          />
        </div>

        {/* Gráfico de comparación entre propiedades */}
        <BarChart
          title="Propiedad - Comparación de Ratings"
          data={propertyRatingsData}
          dataKey="rating"
          nameKey="property"
          barColor="hsl(var(--chart-1))"
          formatValue={(value) => value.toFixed(2)}
        />
      </div>
    </div>
  );
};

export default Dashboard;
