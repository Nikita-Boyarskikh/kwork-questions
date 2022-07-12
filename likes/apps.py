from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class LikesConfig(AppConfig):
    name = 'likes'
    verbose_name = __('Likes')
