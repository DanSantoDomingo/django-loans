from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from . import serializers
from .filtersets import AmortizationScheduleFilter
from .models import AmortizationSchedule, Loan, LoanExcel


class LoanUploadView(ModelViewSet):
    http_method_names = ["post", "get"]
    queryset = LoanExcel.objects.all()
    serializer_class = serializers.LoanExcelSerializer
    lookup_field = "id"


class LoanReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = serializers.LoanSerializer


class AmortizationScheduleViewSet(ReadOnlyModelViewSet):
    queryset = AmortizationSchedule.objects.all().select_related("loan")
    serializer_class = serializers.AmortizationScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AmortizationScheduleFilter
