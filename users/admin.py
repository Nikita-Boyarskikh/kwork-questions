from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from accounts.models import Account
from answers.admin import AnswerInline
from claims.admin import ClaimInline
from likes.admin import LikeInline
from questions.admin import QuestionInline
from users.models import User
from utils.admin import AddingDeniedMixin


class UserAdmin(AddingDeniedMixin, BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                ),
            },
        ),
        (
            _('Personal info'),
            {
                'fields': (
                    'avatar',
                    'country',
                    'preferred_language',
                ),
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_approved',
                    'is_user_agreement_accepted',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            },
        ),
    )
    list_display = ('__str__', 'username', 'preferred_language', 'is_approved', 'is_active', 'is_staff')
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'is_approved',
        'is_user_agreement_accepted',
        'preferred_language',
        'country',
        'groups',
    )
    search_fields = ('username',)
    list_editable = ('is_approved', 'is_active')
    readonly_fields = ('last_login', 'date_joined')
    inlines = (QuestionInline, AnswerInline, LikeInline, ClaimInline)

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            Account.objects.create(user=obj)


admin.site.register(User, UserAdmin)
