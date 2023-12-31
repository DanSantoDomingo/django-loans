from decimal import Decimal

import numpy_financial as npf
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from commons.utils import convert_to_decimal


class LoanExcel(models.Model):
    excel_file = models.FileField()

    def __str__(self) -> str:
        return self.excel_file.name


class PaymentFrequency(models.TextChoices):
    MONTHLY = "Monthly"


class Loan(models.Model):
    loan_number = models.PositiveBigIntegerField(unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    annual_interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    start_date = models.DateField()
    term = models.IntegerField()  # Term in months
    payment_frequency = models.CharField(
        max_length=10,
        choices=PaymentFrequency.choices,
        default=PaymentFrequency.MONTHLY,
    )
    cpr = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    monthly_interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, editable=False
    )
    monthly_payment = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False
    )
    smm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    @property
    def calculate_monthly_interest_rate(self):
        monthly_interest_rate = self.annual_interest_rate / 12
        return monthly_interest_rate

    @property
    def calculate_monthly_payment(self):
        negative = -self.amount
        pmt = npf.pmt(
            convert_to_decimal(self.calculate_monthly_interest_rate),
            self.term,
            negative,
        )
        return pmt

    @property
    def calculate_smm(self):
        # Calculate Single Monthly Mortality
        cpr_decimal = convert_to_decimal(self.cpr)
        smm = (1 - ((1 - cpr_decimal) ** Decimal(1 / 12))) * 100
        return smm

    def __str__(self) -> str:
        return f"Loan {self.loan_number}-{self.amount:,}"

    def save(self, *args, **kwargs):
        self.monthly_interest_rate = self.calculate_monthly_interest_rate
        self.monthly_payment = self.calculate_monthly_payment
        self.smm = self.calculate_smm
        super(Loan, self).save(*args, **kwargs)


class AmortizationSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT)
    period = models.PositiveIntegerField()
    date = models.DateField()
    opening_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0)
    )
    payment = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0)
    )
    pre_payment = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0)
    )
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    monthly_interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    interest = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0)
    )
    principal = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0)
    )
    closing_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal(0)
    )
