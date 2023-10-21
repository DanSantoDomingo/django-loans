from rest_framework import serializers

from .models import LoanExcel
from .tasks import create_loans_and_amortizations


class LoanExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanExcel
        fields = ["excel_file"]

    def create(self, validated_data):
        loan_excel = LoanExcel.objects.create(**validated_data)
        create_loans_and_amortizations.delay(loan_excel.id)
        return loan_excel
