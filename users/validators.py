from django.core.validators import MaxValueValidator

from users.utils import current_year


def max_value_current_year_validator(value):
    current = current_year()
    validator = MaxValueValidator(current)
    return validator(value)
