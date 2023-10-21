from decimal import Decimal


def convert_to_decimal(value: Decimal) -> Decimal:
    return value / 100


def convert_to_percent(value: Decimal) -> Decimal:
    return value * 100
