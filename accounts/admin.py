from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline

from accounts.models import Account, AccountAction


class AccountActionGenericInline(GenericTabularInline):
    model = AccountAction
    extra = 0


class AccountActionInline(TabularInline):
    model = AccountAction
    extra = 0


class AccountAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'balance', 'uid')
    search_fields = ('uid', 'user__username', 'user__email')
    list_select_related = ('user',)
    ordering = ('-balance',)
    readonly_fields = ('balance', 'created', 'modified')
    inlines = [AccountActionInline]


class AccountActionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'uid', 'type', 'delta', 'created', 'status', 'account', 'product')
    list_editable = ('status',)
    list_filter = ('account', 'type', 'status')
    search_fields = ('uid', 'account__uid', 'account__user__username', 'account__user__email', 'comment')
    readonly_fields = ('uid', 'created', 'modified')
    list_select_related = ('account', 'account__user')


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountAction, AccountActionAdmin)
