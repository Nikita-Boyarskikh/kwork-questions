from urllib.parse import urlparse

from annoying.functions import get_object_or_None
from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import resolve_url


class AccessWithMessageMixin(AccessMixin):
    def handle_no_permission(self):
        permission_denied_message = self.get_permission_denied_message()
        if permission_denied_message:
            messages.error(self.request, permission_denied_message)

        # NOTE: next lines copy-pasted from django/contrib/auth/mixins.py:50
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class AccessWithMessageAdapter(AccessWithMessageMixin):
    def __init__(self, redirect_url=None, permission_denied_message=None):
        self.login_url = redirect_url
        self.permission_denied_message = permission_denied_message

    def permission_denied_response(self, request):
        self.request = request
        return super().handle_no_permission()


class UserAgreementRequiredMixin:
    accept_agreements_url = None
    agreements_not_accepted_message = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_user_agreement_accepted:
            adapter = AccessWithMessageAdapter(self.accept_agreements_url, self.agreements_not_accepted_message)
            return adapter.permission_denied_response(request)
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(DjangoLoginRequiredMixin, AccessWithMessageMixin):
    pass


class CurrentCountryListViewMixin:
    country_field_name = 'country_id'

    def get_queryset(self):
        qs = super().get_queryset()
        country_id = self.kwargs.get('country_id')
        if not country_id or country_id == 'unknown':
            return qs
        return qs.filter(**{self.country_field_name: country_id})


class MyListViewMixin(LoginRequiredMixin):
    owner_field_name = 'author'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(**{self.owner_field_name: self.request.user})


class ForGenericMixin:
    content_type_field = 'content_type'
    object_id_field = 'object_id'

    def get_queryset(self):
        qs = super().get_queryset()
        model_name = self.kwargs.get('content_type')
        content_type = get_object_or_None(ContentType.objects.filter(app_label=f'{model_name}s', model=model_name))
        return qs.filter(**{
            self.content_type_field: content_type,
            self.object_id_field: self.kwargs.get('object_id'),
        })
