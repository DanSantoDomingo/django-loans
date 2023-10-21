from django.contrib import admin

from loans.models import Loan


# Register your models here.
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ["monthly_interest_rate", "monthly_payment", "smm"]
