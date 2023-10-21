import logging
from decimal import Decimal
from typing import List

import pandas as pd
from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import transaction

from commons.utils import convert_to_decimal, convert_to_percent

from .models import AmortizationSchedule, Loan, LoanExcel

logger = logging.getLogger(__name__)


@shared_task
def create_loans_and_amortizations(upload_id: int):
    file: LoanExcel = LoanExcel.objects.get(id=upload_id)
    df = pd.read_excel(file.excel_file.file, sheet_name=0)
    df.columns = df.columns.str.strip()
    df = df.loc[1:]
    for index, row in df.iterrows():
        loan_number = row[settings.LOAN_NUMBER]
        logger.info("Creating Loan Number: %s", loan_number)
        loan = Loan.objects.create(
            loan_number=int(loan_number),
            amount=Decimal(row[settings.LOAN_AMOUNT]),
            annual_interest_rate=convert_to_percent(
                Decimal(row[settings.INTEREST_RATE])
            ),
            start_date=row[settings.START_DATE],
            term=int(row[settings.PAYMENT_TERM]),
            payment_frequency=row[settings.PAY_FREQUENCY],
            cpr=convert_to_percent(Decimal(row[settings.CPR])),
        )
        logger.info("Created Loan Number: %s", loan_number)

        create_loan_amortization_schedule.delay(loan.id)

    logger.info("Processing `%s` completed.", file.excel_file.name)


@shared_task
def create_loan_amortization_schedule(loan_id: int):
    loan = Loan.objects.get(id=loan_id)
    logger.info(
        "Creating Amortization Schedules for Loan Number: %s", loan.loan_number
    )
    schedules: List[AmortizationSchedule] = []
    for period in range(loan.term + 1):
        if not schedules:
            # Create the initial schedule
            schedules.append(
                AmortizationSchedule(
                    loan=loan,
                    period=period,
                    date=loan.start_date,
                    interest_rate=Decimal(),
                    monthly_interest_rate=Decimal(),
                    closing_balance=loan.amount,
                )
            )
            continue

        loan_monthly_payment = loan.calculate_monthly_payment
        loan_smm = loan.calculate_smm

        previous: AmortizationSchedule = schedules[-1]
        opening_balance = previous.closing_balance

        interest_rate: Decimal = (
            loan.annual_interest_rate
            if opening_balance > Decimal()
            else Decimal()
        )

        monthly_interest_rate: Decimal = interest_rate / 12

        interest: Decimal = opening_balance * convert_to_decimal(
            interest_rate / 12
        )

        payment: Decimal = min(loan_monthly_payment, opening_balance + interest)

        pre_payment: Decimal = (
            Decimal(0)
            if payment < loan_monthly_payment
            else opening_balance * convert_to_decimal(loan_smm)
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

    logger.info(
        "Created Amortization Schedules for Loan Number: %s", loan.loan_number
    )
