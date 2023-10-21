from rest_framework import serializers

from .models import AmortizationSchedule, Loan, LoanExcel
from .tasks import create_loans_and_amortizations


class LoanExcelSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="loan-uploads-detail", lookup_field="id"
    )

    class Meta:
        model = LoanExcel
        fields = ["id", "url", "excel_file"]

    def create(self, validated_data):
        loan_excel = LoanExcel.objects.create(**validated_data)
        create_loans_and_amortizations.delay(loan_excel.id)
        return loan_excel


class LoanSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="loans-detail", lookup_field="id"
    )

    class Meta:
        model = Loan
        fields = [
            "id",
            "url",
            "loan_number",
            "amount",
            "annual_interest_rate",
            "start_date",
            "term",
            "payment_frequency",
            "cpr",
            "monthly_interest_rate",
            "monthly_payment",
            "smm",
        ]


class AmortizationScheduleSerializer(serializers.ModelSerializer):
    loan = LoanSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name="amortizations-detail", lookup_field="id"
    )

    class Meta:
        model = AmortizationSchedule
        fields = [
            "id",
            "url",
            "period",
            "date",
            "opening_balance",
            "payment",
            "pre_payment",
            "interest_rate",
            "monthly_interest_rate",
            "interest",
            "principal",
            "closing_balance",
            "loan",
        ]
