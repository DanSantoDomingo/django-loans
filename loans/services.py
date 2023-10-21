from decimal import Decimal
from typing import List

from dateutil.relativedelta import relativedelta
from django.db import transaction

from commons.utils import convert_to_decimal
from loans.models import AmortizationSchedule, Loan


def create_loan_amortization_schedule(loan: Loan):
    schedules: List[AmortizationSchedule] = []
    for period in range(loan.term + 1):
        if not schedules:
            # Create the initial schedule
            schedules.append(
                AmortizationSchedule(
                    loan=loan,
                    period=period,
                    date=loan.start_date,
                    interest_rate=Decimal(0),
                    monthly_interest_rate=Decimal(0),
                    closing_balance=loan.amount,
                )
            )
            continue

        previous: AmortizationSchedule = schedules[-1]
        opening_balance = previous.closing_balance.quantize(Decimal("0.00"))
        interest_rate: Decimal = (
            loan.annual_interest_rate
            if opening_balance > Decimal("0.00")
            else Decimal("0.00")
        )
        monthly_interest_rate: Decimal = (interest_rate / 12).quantize(
            Decimal("0.00")
        )
        interest: Decimal = (
            opening_balance * convert_to_decimal(monthly_interest_rate)
        ).quantize(Decimal("0.00"))
        payment: Decimal = min(
            loan.monthly_payment, opening_balance + interest
        ).quantize(Decimal("0.00"))
        pre_payment: Decimal = (
            Decimal(0)
            if payment < loan.monthly_payment
            else opening_balance * convert_to_decimal(loan.smm)
        )
        principal: Decimal = payment + (pre_payment - interest)
        closing_balance: Decimal = opening_balance - principal
        next = AmortizationSchedule(
            loan=loan,
            period=period,
            date=previous.date + relativedelta(months=1),
            opening_balance=opening_balance,
            interest_rate=interest_rate,
            monthly_interest_rate=monthly_interest_rate,
            interest=interest,
            payment=payment,
            pre_payment=pre_payment,
            principal=principal,
            closing_balance=closing_balance,
        )

        schedules.append(next)

    with transaction.atomic():
        AmortizationSchedule.objects.bulk_create(schedules)
