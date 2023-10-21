from rest_framework import serializers

from .models import Loan, LoanExcel
from .tasks import create_loans_and_amortizations


class LoanExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanExcel
        fields = ["excel_file"]

    def create(self, validated_data):
        loan_excel = LoanExcel.objects.create(**validated_data)
        create_loans_and_amortizations.delay(loan_excel.id)
        return loan_excel


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
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
