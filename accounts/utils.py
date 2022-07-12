from django.conf import settings
from djmoney.money import Money


def zero_money(currency=settings.DEFAULT_CURRENCY):
    return Money(0, currency=currency)
