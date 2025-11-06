from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.metrics_service import calculate_metrics

class DashboardMetricsAPIView(APIView):
    def get(self, request):
        property_ = request.GET.get("property", "all")
        area = request.GET.get("area", "all")
        
        print(f"🔍 ===== DEBUGGING FRONTEND FILTERS =====")
        print(f"📄 Todos los parámetros GET: {dict(request.GET)}")
        print(f"🏨 Property: '{property_}'")
        print(f"📍 Area: '{area}'")
        
        # Construir filtro de período jerárquico
        period_filter = {}
        
        # Obtener parámetros de fecha jerárquicos
        year = request.GET.get("year")
        quarter = request.GET.get("quarter") 
        month = request.GET.get("month")
        day = request.GET.get("day")
        
        print(f"📅 Filtros de fecha recibidos:")
        print(f"   Year: {year}")
        print(f"   Quarter: {quarter}")
        print(f"   Month: {month}")
        print(f"   Day: {day}")
        
        # Si no hay filtros jerárquicos, usar el período simple por compatibilidad
        if not any([year, quarter, month, day]):
            period_filter = request.GET.get("period", "month")
            print(f"📅 Usando período simple: {period_filter}")
        else:
            # Construir filtro jerárquico
            if year:
                period_filter['year'] = int(year)
            if quarter:
                period_filter['quarter'] = int(quarter)  
            if month:
                period_filter['month'] = int(month)
            if day:
                period_filter['day'] = int(day)
            print(f"📅 Filtro jerárquico construido: {period_filter}")

        print(f"🔍 API va a calcular métricas con: property={property_}, area={area}, period={period_filter}")
        print("🔍 ========================================")

        try:
            metrics = calculate_metrics(property_, area, period_filter)
            print(f"✅ Métricas calculadas exitosamente")
            print(f"📊 Métricas obtenidas: {metrics}")
            
            return Response({
                "property": property_,
                "area": area,
                "period": period_filter,
                "metrics": metrics
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ ERROR en DashboardMetricsAPIView: {e}")
            print(f"❌ Tipo de error: {type(e)}")
            import traceback
            traceback.print_exc()
            
            return Response({
                "error": str(e),
                "property": property_,
                "area": area,
                "period": period_filter,
                "metrics": {
                    "%ocupacion": 0,
                    "ventas_totales": 0
                }
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
