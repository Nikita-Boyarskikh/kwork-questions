from constance import config
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def min_question_price_validator(value):
    return min_question_price_amount_validator(value.amount)


def min_question_price_amount_validator(value):
    if value < config.MIN_QUESTION_PRICE:
        raise ValidationError(
            message=_('Ensure this value is greater than or equal to %(limit_value)s.'),
            params={
                'limit_value': config.MIN_QUESTION_PRICE,
            },
            code='min_price',
        )
