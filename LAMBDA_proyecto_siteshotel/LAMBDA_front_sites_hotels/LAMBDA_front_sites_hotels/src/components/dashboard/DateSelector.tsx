/**
 * DateSelector - Selector de Fecha Jerárquico (Como Power BI)
 * 
 * Componente que replica la estructura jerárquica de Power BI:
 * - Año (2025, 2024, etc.)
 *   - Trimestre (Qtr 1, Qtr 2, Qtr 3, Qtr 4)
 *     - Mes (enero, febrero, marzo, etc.)
 *       - Día (1, 2, 3, etc.)
 */

import React, { useState } from 'react';
import { useFilters, DateFilter } from '@/contexts/FilterContext';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Calendar, ChevronDown } from 'lucide-react';

/**
 * Componente DateSelector
 */
export const DateSelector: React.FC = () => {
  const { dateFilter, setDateFilter } = useFilters();
  const [isExpanded, setIsExpanded] = useState(false);

  // Generar años disponibles (desde 2012 hasta año actual + 1)
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: currentYear - 2012 + 2 }, (_, i) => 2012 + i);

  // Trimestres
  const quarters = [
    { value: 1, label: 'Qtr 1', months: [1, 2, 3] },
    { value: 2, label: 'Qtr 2', months: [4, 5, 6] },
    { value: 3, label: 'Qtr 3', months: [7, 8, 9] },
    { value: 4, label: 'Qtr 4', months: [10, 11, 12] },
  ];

  // Meses del año
  const months = [
    { value: 1, label: 'enero', quarter: 1 },
    { value: 2, label: 'febrero', quarter: 1 },
    { value: 3, label: 'marzo', quarter: 1 },
    { value: 4, label: 'abril', quarter: 2 },
    { value: 5, label: 'mayo', quarter: 2 },
    { value: 6, label: 'junio', quarter: 2 },
    { value: 7, label: 'julio', quarter: 3 },
    { value: 8, label: 'agosto', quarter: 3 },
    { value: 9, label: 'septiembre', quarter: 3 },
    { value: 10, label: 'octubre', quarter: 4 },
    { value: 11, label: 'noviembre', quarter: 4 },
    { value: 12, label: 'diciembre', quarter: 4 },
  ];

  // Obtener meses disponibles según trimestre seleccionado
  const getAvailableMonths = () => {
    if (!dateFilter.quarter) return months;
    return months.filter(month => month.quarter === dateFilter.quarter);
  };

  // Generar días del mes seleccionado
  const getDaysInMonth = (year: number, month: number) => {
    const daysInMonth = new Date(year, month, 0).getDate();
    return Array.from({ length: daysInMonth }, (_, i) => i + 1);
  };

  // Actualizar filtro con lógica jerárquica
  const updateFilter = (updates: Partial<DateFilter>) => {
    let newFilter = { ...dateFilter, ...updates };
    
    // Si cambia el año, resetear trimestre, mes y día
    if (updates.year !== undefined && updates.year !== dateFilter.year) {
      newFilter = { year: updates.year, quarter: undefined, month: undefined, day: undefined };
    }
    
    // Si cambia el trimestre, resetear mes y día
    if (updates.quarter !== undefined && updates.quarter !== dateFilter.quarter) {
      newFilter = { ...newFilter, quarter: updates.quarter, month: undefined, day: undefined };
    }
    
    // Si cambia el mes, resetear día y actualizar trimestre si es necesario
    if (updates.month !== undefined && updates.month !== dateFilter.month) {
      const monthData = months.find(m => m.value === updates.month);
      newFilter = { 
        ...newFilter, 
        month: updates.month, 
        quarter: monthData?.quarter,
        day: undefined 
      };
    }
    
    setDateFilter(newFilter);
  };

  // Formatear etiqueta para mostrar la selección actual
  const getDateLabel = () => {
    const parts = [];
    
    if (dateFilter.year) {
      parts.push(dateFilter.year.toString());
    }
    
    if (dateFilter.quarter) {
      const quarterLabel = quarters.find(q => q.value === dateFilter.quarter)?.label;
      parts.push(quarterLabel);
    }
    
    if (dateFilter.month) {
      const monthLabel = months.find(m => m.value === dateFilter.month)?.label;
      parts.push(monthLabel);
    }
    
    if (dateFilter.day) {
      parts.push(dateFilter.day.toString());
    }
    
    return parts.length > 0 ? parts.join(' > ') : 'Todas las fechas';
  };

  return (
    <div className="flex items-center gap-2">
      <Calendar className="w-5 h-5 text-muted-foreground" />
      
      {/* Selector principal */}
      <div className="relative">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-2 px-3 py-2 bg-background border border-border rounded-md hover:bg-accent hover:text-accent-foreground min-w-[250px] justify-between"
        >
          <span className="text-sm">{getDateLabel()}</span>
          <ChevronDown className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
        </button>

        {/* Panel expandido */}
        {isExpanded && (
          <div className="absolute top-full left-0 mt-1 bg-popover border border-border rounded-md shadow-lg z-50 p-4 min-w-[350px]">
            
            {/* Selector de Año */}
            <div className="mb-4">
              <label className="text-sm font-medium text-foreground block mb-2">Año</label>
              <Select
                value={dateFilter.year?.toString()}
                onValueChange={(value) => updateFilter({ year: parseInt(value) })}
              >
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Seleccionar año" />
                </SelectTrigger>
                <SelectContent className="max-h-[200px]">
                  {years.reverse().map((year) => (
                    <SelectItem key={year} value={year.toString()}>
                      {year}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Selector de Trimestre */}
            {dateFilter.year && (
              <div className="mb-4">
                <label className="text-sm font-medium text-foreground block mb-2">Trimestre</label>
                <Select
                  value={dateFilter.quarter?.toString()}
                  onValueChange={(value) => updateFilter({ quarter: parseInt(value) })}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Seleccionar trimestre" />
                  </SelectTrigger>
                  <SelectContent>
                    {quarters.map((quarter) => (
                      <SelectItem key={quarter.value} value={quarter.value.toString()}>
                        {quarter.label} ({months.filter(m => m.quarter === quarter.value).map(m => m.label).join(', ')})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {/* Selector de Mes */}
            {(dateFilter.year && dateFilter.quarter) && (
              <div className="mb-4">
                <label className="text-sm font-medium text-foreground block mb-2">Mes</label>
                <Select
                  value={dateFilter.month?.toString()}
                  onValueChange={(value) => updateFilter({ month: parseInt(value) })}
                >
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
            {(dateFilter.year && dateFilter.month) && (
              <div className="mb-4">
                <label className="text-sm font-medium text-foreground block mb-2">Día</label>
                <Select
                  value={dateFilter.day?.toString()}
                  onValueChange={(value) => updateFilter({ day: parseInt(value) })}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Seleccionar día" />
                  </SelectTrigger>
                  <SelectContent className="max-h-[200px]">
                    {getDaysInMonth(dateFilter.year, dateFilter.month).map((day) => (
                      <SelectItem key={day} value={day.toString()}>
                        {day}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}

            {/* Botones de acción */}
            <div className="flex justify-end gap-2 pt-2 border-t border-border">
              <button
                onClick={() => {
                  setDateFilter({
                    year: undefined,
                    quarter: undefined,
                    month: undefined,
                    day: undefined,
                  });
                }}
                className="px-3 py-1 text-sm text-muted-foreground hover:text-foreground"
              >
                Limpiar
              </button>
              <button
                onClick={() => setIsExpanded(false)}
                className="px-3 py-1 text-sm bg-primary text-primary-foreground rounded hover:bg-primary/90"
              >
                Aplicar
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};