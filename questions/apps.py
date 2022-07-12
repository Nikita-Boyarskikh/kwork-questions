from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class QuestionsConfig(AppConfig):
    name = 'questions'
    verbose_name = __('Questions')
