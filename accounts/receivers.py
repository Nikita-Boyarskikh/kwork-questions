from accounts.models import AccountAction, AccountActionStatus


def before_account_action_saved(instance, **kwargs):
    is_new = not instance.pk
    is_approved = instance.status == AccountActionStatus.APPROVED
    delta = instance.delta

    if is_new and not is_approved:
        return

    if not is_new:
        previous = AccountAction.objects.get(pk=instance.pk)
        was_approved = previous.status == AccountActionStatus.APPROVED
        if previous.status == instance.status or not is_approved and not was_approved:
            return
        if was_approved:
            delta = -delta

    instance.account.balance += delta
    instance.account.save(update_fields=('balance',))
