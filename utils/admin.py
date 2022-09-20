class AddingDeniedMixin:
    def has_add_permission(self, request, obj=None):
        return False


class ChangingDeniedMixin:
    def has_change_permission(self, request, obj=None):
        return False


class DeletingDeniedMixin:
    def has_delete_permission(self, request, obj=None):
        return False
