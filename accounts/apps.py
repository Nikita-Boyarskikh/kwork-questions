from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as __


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = __('Accounting')

    def ready(self):
        from accounts.receivers import before_account_action_saved
        from accounts.models import AccountAction

        pre_save.connect(
            before_account_action_saved,
            sender=AccountAction,
            dispatch_uid=before_account_action_saved.__name__
        )
