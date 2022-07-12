from datetime import date

from django.utils.translation import get_language, get_language_from_request

from languages.models import Language


def current_year():
    return date.today().year


def get_current_language(user, request):
    if user and user.preferred_language:
        return user.preferred_language

    if user and user.country is not None:
        return user.country.language

    current_language_code = get_language_from_request(request)
    return Language.objects.get(current_language_code)
