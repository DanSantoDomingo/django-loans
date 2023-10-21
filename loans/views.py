from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from . import serializers
from .filtersets import AmortizationScheduleFilter
from .models import AmortizationSchedule, Loan


class LoanUploadView(CreateAPIView):
    serializer_class = serializers.LoanExcelSerializer


class LoanReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = serializers.LoanSerializer


class AmortizationScheduleViewSet(ReadOnlyModelViewSet):
    queryset = AmortizationSchedule.objects.all().select_related("loan")
    serializer_class = serializers.AmortizationScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AmortizationScheduleFilter
