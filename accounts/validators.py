from accounts.utils import zero_money


def not_zero_money_validator(money):
    return money != zero_money()
