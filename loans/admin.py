from django.contrib import admin

from loans.models import AmortizationSchedule, Loan


# Register your models here.
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ["monthly_interest_rate", "monthly_payment", "smm"]


@admin.register(AmortizationSchedule)
class AmortizationScheduleAdmin(admin.ModelAdmin):
    list_filter = ["loan"]
    list_display = [
        "id",
        "loan",
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
    ]
