from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.metrics_service import calculate_metrics

class DashboardMetricsAPIView(APIView):
    def get(self, request):
        property_ = request.GET.get("property", "all")
        concept = request.GET.get("concept", "all")
        period = request.GET.get("period", "month")

        metrics = calculate_metrics(property_, concept, period)
        return Response({
            "property": property_,
            "concept": concept,
            "period": period,
            "metrics": metrics
        }, status=status.HTTP_200_OK)
