from django.apps import AppConfig
from django.utils.translation import gettext_lazy as __


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = __('Users')
