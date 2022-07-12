from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class LanguagesConfig(AppConfig):
    name = 'languages'
    verbose_name = __('Languages')
