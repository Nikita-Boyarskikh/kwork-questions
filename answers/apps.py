from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class AnswersConfig(AppConfig):
    name = 'answers'
    verbose_name = __('Answers')
