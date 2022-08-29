from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class RulesConfig(AppConfig):
    name = 'rules'
    verbose_name = __('Rules')
