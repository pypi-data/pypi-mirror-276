from decimal import Decimal


def apply_slippage(amount: int, slippage: Decimal) -> int:
    min_amount = int(Decimal(amount) * (Decimal(1) - (slippage / Decimal(100))))
    return min_amount
