/**
 * DateHierarchySelector - Selector Jerárquico de Fechas
 * 
 * Componente que permite seleccionar fechas de manera jerárquica:
 * Año > Trimestre > Mes > Día
 * 
 * Similar al comportamiento de Power BI donde puedes expandir
 * cada nivel para hacer selecciones más específicas
 */

import React, { useState, useEffect } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Calendar, ChevronDown, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

// Tipos para la selección jerárquica
export interface DateSelection {
  year?: number;
  quarter?: number;
  month?: number;
  day?: number;
  mode: 'year' | 'quarter' | 'month' | 'day';
}

interface DateHierarchySelectorProps {
  value: DateSelection;
  onChange: (selection: DateSelection) => void;
  className?: string;
}

// Datos de referencia
const QUARTERS = [
  { value: 1, label: 'Q1 (Ene-Mar)', months: [1, 2, 3] },
  { value: 2, label: 'Q2 (Abr-Jun)', months: [4, 5, 6] },
  { value: 3, label: 'Q3 (Jul-Sep)', months: [7, 8, 9] },
  { value: 4, label: 'Q4 (Oct-Dic)', months: [10, 11, 12] },
];

const MONTHS = [
  { value: 1, label: 'Enero', quarter: 1 },
  { value: 2, label: 'Febrero', quarter: 1 },
  { value: 3, label: 'Marzo', quarter: 1 },
  { value: 4, label: 'Abril', quarter: 2 },
  { value: 5, label: 'Mayo', quarter: 2 },
  { value: 6, label: 'Junio', quarter: 2 },
  { value: 7, label: 'Julio', quarter: 3 },
  { value: 8, label: 'Agosto', quarter: 3 },
  { value: 9, label: 'Septiembre', quarter: 3 },
  { value: 10, label: 'Octubre', quarter: 4 },
  { value: 11, label: 'Noviembre', quarter: 4 },
  { value: 12, label: 'Diciembre', quarter: 4 },
];

// Obtener días del mes
const getDaysInMonth = (year: number, month: number): number[] => {
  const daysInMonth = new Date(year, month, 0).getDate();
  return Array.from({ length: daysInMonth }, (_, i) => i + 1);
};

export const DateHierarchySelector: React.FC<DateHierarchySelectorProps> = ({
  value,
  onChange,
  className,
}) => {
  const [availableYears] = useState(() => {
    // Generar años desde 2020 hasta año actual + 1
    const currentYear = new Date().getFullYear();
    return Array.from({ length: currentYear - 2019 }, (_, i) => 2020 + i);
  });

  // Manejadores de cambio
  const handleYearChange = (year: string) => {
    const yearNum = parseInt(year);
    onChange({
      year: yearNum,
      mode: 'year',
    });
  };

  const handleQuarterChange = (quarter: string) => {
    const quarterNum = parseInt(quarter);
    onChange({
      ...value,
      quarter: quarterNum,
      mode: 'quarter',
    });
  };

  const handleMonthChange = (month: string) => {
    const monthNum = parseInt(month);
    onChange({
      ...value,
      month: monthNum,
      mode: 'month',
    });
  };

  const handleDayChange = (day: string) => {
    const dayNum = parseInt(day);
    onChange({
      ...value,
      day: dayNum,
      mode: 'day',
    });
  };

  // Filtrar meses según el trimestre seleccionado
  const getAvailableMonths = () => {
    if (!value.quarter) return MONTHS;
    return MONTHS.filter(month => month.quarter === value.quarter);
  };

  // Obtener días disponibles
  const getAvailableDays = () => {
    if (!value.year || !value.month) return [];
    return getDaysInMonth(value.year, value.month);
  };

  // Generar texto de resumen
  const getSummaryText = () => {
    if (value.mode === 'day' && value.year && value.month && value.day) {
      const monthName = MONTHS.find(m => m.value === value.month)?.label;
      return `${value.day} de ${monthName} ${value.year}`;
    }
    if (value.mode === 'month' && value.year && value.month) {
      const monthName = MONTHS.find(m => m.value === value.month)?.label;
      return `${monthName} ${value.year}`;
    }
    if (value.mode === 'quarter' && value.year && value.quarter) {
      const quarterInfo = QUARTERS.find(q => q.value === value.quarter);
      return `${quarterInfo?.label} ${value.year}`;
    }
    if (value.mode === 'year' && value.year) {
      return `Año ${value.year}`;
    }
    return 'Seleccionar fecha';
  };

  return (
    <Card className={className}>
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2 text-sm">
          <Calendar className="w-4 h-4" />
          Período de Análisis
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {/* Resumen de selección */}
        <div className="text-sm font-medium text-foreground bg-muted/50 p-2 rounded">
          {getSummaryText()}
        </div>

        {/* Selector de Año */}
        <div className="space-y-2">
          <label className="text-xs font-medium text-muted-foreground">Año</label>
          <Select value={value.year?.toString()} onValueChange={handleYearChange}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Seleccionar año" />
            </SelectTrigger>
            <SelectContent>
              {availableYears.map((year) => (
                <SelectItem key={year} value={year.toString()}>
                  {year}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Selector de Trimestre */}
        {value.year && (
          <div className="space-y-2">
            <label className="text-xs font-medium text-muted-foreground">Trimestre</label>
            <Select value={value.quarter?.toString()} onValueChange={handleQuarterChange}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Seleccionar trimestre" />
              </SelectTrigger>
              <SelectContent>
                {QUARTERS.map((quarter) => (
                  <SelectItem key={quarter.value} value={quarter.value.toString()}>
                    {quarter.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Selector de Mes */}
        {value.year && value.quarter && (
          <div className="space-y-2">
            <label className="text-xs font-medium text-muted-foreground">Mes</label>
            <Select value={value.month?.toString()} onValueChange={handleMonthChange}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Seleccionar mes" />
              </SelectTrigger>
              <SelectContent>
                {getAvailableMonths().map((month) => (
                  <SelectItem key={month.value} value={month.value.toString()}>
                    {month.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Selector de Día */}
        {value.year && value.month && (
          <div className="space-y-2">
            <label className="text-xs font-medium text-muted-foreground">Día</label>
            <Select value={value.day?.toString()} onValueChange={handleDayChange}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Seleccionar día" />
              </SelectTrigger>
              <SelectContent className="max-h-48 overflow-y-auto">
                {getAvailableDays().map((day) => (
                  <SelectItem key={day} value={day.toString()}>
                    {day}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Botón para limpiar selección */}
        <button
          onClick={() => onChange({ mode: 'year' })}
          className="text-xs text-muted-foreground hover:text-foreground transition-colors"
        >
          Limpiar selección
        </button>
      </CardContent>
    </Card>
  );
};