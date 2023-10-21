import django_filters

from .models import AmortizationSchedule


class AmortizationScheduleFilter(django_filters.FilterSet):
    loan_number = django_filters.NumberFilter(
        field_name="loan__loan_number", lookup_expr="exact"
    )
    ordering = django_filters.OrderingFilter(
        fields=(("period", "period"),),
    )

    class Meta:
        model = AmortizationSchedule
        fields = ["loan_number"]
