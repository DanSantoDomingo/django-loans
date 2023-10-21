from rest_framework import serializers

from .models import LoanExcel


class LoanExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanExcel
        fields = ["excel_file"]

    def create(self, validated_data):
        loan_excel = LoanExcel.objects.create(**validated_data)

        return loan_excel
