from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class ChatConfig(AppConfig):
    name = 'chat'
    verbose_name = __('Chat')
