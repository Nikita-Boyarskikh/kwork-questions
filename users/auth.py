from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import user_email, user_username

from accounts.models import Account
from languages.models import Language


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user_username(user, data.get('username'))
        user.preferred_language = Language.get_for_request(request)

        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()

        self.populate_username(request, user)
        if commit:
            user.save()
            Account.objects.create(user=user)
        return user
