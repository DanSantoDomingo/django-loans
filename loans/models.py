from decimal import Decimal

import numpy_financial as npf
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from commons.utils import convert_to_decimal


class PaymentFrequency(models.TextChoices):
    MONTHLY = "Monthly"


class Loan(models.Model):
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

    def _calculate_monthly_interest_rate(self):
        monthly_interest_rate = self.annual_interest_rate / 12
        return monthly_interest_rate

    def _calculate_monthly_payment(self):
        negative = -self.amount
        return npf.pmt(
            convert_to_decimal(self.monthly_interest_rate), self.term, negative
        )

    def _calculate_smm(self):
        # Calculate Single Monthly Mortality
        cpr_decimal = convert_to_decimal(self.cpr)
        smm = (1 - ((1 - cpr_decimal) ** Decimal(1 / 12))) * 100
        return smm

    def save(self, *args, **kwargs):
        self.monthly_interest_rate = self._calculate_monthly_interest_rate()
        self.monthly_payment = self._calculate_monthly_payment()
        self.smm = self._calculate_smm()
        super(Loan, self).save(*args, **kwargs)


class AmortizationSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
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
