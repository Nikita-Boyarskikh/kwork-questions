from datetime import date

from django.core.validators import MaxValueValidator


def max_value_current_year_validator(value):
    current = date.today().year
    validator = MaxValueValidator(current)
    return validator(value)
