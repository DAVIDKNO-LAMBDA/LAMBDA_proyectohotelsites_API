/**
 * FilterBar - Barra de Filtros Global
 * 
 * Este componente proporciona controles de filtrado que afectan
 * todos los datos mostrados en el dashboard:
 * - Selector de fecha jerárquico (año, trimestre, mes, día)
 * - Selector de sede/propiedad (Sites 45, BAQ, Group, Recreo)
 * - Selector de área (Alojamiento, Restaurante, etc.)
 * 
 * Los filtros se sincronizan con el FilterContext para que todos
 * los componentes de la aplicación reaccionen a los cambios
 */

import React from 'react';
import { useFilters, PropertyType, AreaType } from '@/contexts/FilterContext';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Building2, MapPin } from 'lucide-react';
import { DateSelector } from './DateSelector';

/**
 * Componente FilterBar
 */
export const FilterBar: React.FC = () => {
  // Obtener el estado y funciones del contexto de filtros
  const { property, setProperty, area, setArea } = useFilters();

  // Opciones de propiedad disponibles (basadas en las imágenes)
  const propertyOptions: { value: PropertyType; label: string }[] = [
    { value: 'all', label: 'Todas' },
    { value: 'sites45', label: 'Sites 45' },
    { value: 'sitesBAQ', label: 'Sites BAQ' },
    { value: 'sitesGroup', label: 'Sites Group' },
    { value: 'sitesRecreo', label: 'Sites Recreo' },
  ];

  // Opciones de área disponibles
  const areaOptions: { value: AreaType; label: string }[] = [
    { value: 'all', label: 'Todas las áreas' },
    { value: 'evento', label: 'Eventos' },
    { value: 'lavanderia', label: 'Lavandería' },
    { value: 'minibar', label: 'Minibar' },
    { value: 'restaurante', label: 'Restaurante' },
    { value: 'roomservice', label: 'Room Service' },
    { value: 'alojamiento', label: 'Alojamiento' },
  ];

  return (
    <div className="flex flex-wrap items-center gap-4 p-4 bg-card rounded-lg border shadow-sm">
      
      {/* Selector de Fecha Jerárquico */}
      <DateSelector />

      {/* Selector de Propiedad/Sede */}
      <div className="flex items-center gap-2">
        <Building2 className="w-5 h-5 text-muted-foreground" />
        <Select value={property} onValueChange={(value) => setProperty(value as PropertyType)}>
          <SelectTrigger className="w-[180px] bg-background">
            <SelectValue placeholder="Seleccionar propiedad" />
          </SelectTrigger>
          <SelectContent className="bg-popover z-50">
            {propertyOptions.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Selector de Área */}
      <div className="flex items-center gap-2">
        <MapPin className="w-5 h-5 text-muted-foreground" />
        <Select value={area} onValueChange={(value) => setArea(value as AreaType)}>
          <SelectTrigger className="w-[180px] bg-background">
            <SelectValue placeholder="Seleccionar área" />
          </SelectTrigger>
          <SelectContent className="bg-popover z-50">
            {areaOptions.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Información del filtro activo */}
      <div className="ml-auto text-sm text-muted-foreground">
        Filtros activos: 
        <span className="font-medium text-foreground ml-1">
          {propertyOptions.find(p => p.value === property)?.label}
        </span>
        {area !== 'all' && (
          <span> - <span className="font-medium text-foreground">
            {areaOptions.find(a => a.value === area)?.label}
          </span></span>
        )}
      </div>
    </div>
  );
};