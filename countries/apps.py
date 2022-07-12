from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class CountriesConfig(AppConfig):
    name = 'countries'
    verbose_name = __('Countries')
