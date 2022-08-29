from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from answers.admin import AnswerInline
from claims.admin import ClaimInline
from likes.admin import LikeInline
from questions.admin import QuestionInline
from users.auth import AccountAdapter, send_email_confirmation
from users.models import User


class UserAdmin(BaseUserAdmin):
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
                    'email',
                    'avatar',
                    'birth_year',
                    'sex',
                    'education',
                    'country',
                    'preferred_language',
                ),
            },
        ),
        (
            _('Payment info'),
            {
                'fields': (
                    'pin',
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
        )
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2', 'pin', 'preferred_language'),
            },
        ),
    )
    list_display = ('__str__', 'username', 'email', 'preferred_language', 'is_approved', 'is_active', 'is_staff')
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'is_approved',
        'is_user_agreement_accepted',
        'preferred_language',
        'country',
        'sex',
        'education',
        'groups',
    )
    search_fields = ('username', 'email')
    list_editable = ('is_approved', 'is_active')
    readonly_fields = ('last_login', 'date_joined')
    inlines = [QuestionInline, AnswerInline, LikeInline, ClaimInline]

    def save_model(self, request, obj, form, change):
        user = AccountAdapter(request).save_user(request, obj, form)
        send_email_confirmation(user)


admin.site.register(User, UserAdmin)
