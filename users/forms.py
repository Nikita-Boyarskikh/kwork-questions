from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from django import forms
from allauth.account.forms import PasswordField
from django.utils.translation import gettext as _
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_username


class SignupForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Username"),
        min_length=1,
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": _("Username"), "autocomplete": "username"}
        ),
    )
    password1 = PasswordField(label=_("Password"), autocomplete="new-password")
    password2 = PasswordField(label=_("Password (again)"), autocomplete="new-password")
    captcha = CaptchaField()

    def clean_username(self):
        value = self.cleaned_data["username"]
        value = get_adapter().clean_username(value)
        return value

    def clean(self):
        super().clean()

        # `password` cannot be of type `SetPasswordField`, as we don't
        # have a `User` yet. So, let's populate a dummy user to be used
        # for password validaton.
        User = get_user_model()
        dummy_user = User()
        user_username(dummy_user, self.cleaned_data.get("username"))
        password = self.cleaned_data.get("password1")
        if password:
            try:
                get_adapter().clean_password(password, user=dummy_user)
            except forms.ValidationError as e:
                self.add_error("password1", e)

        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                self.add_error(
                    "password2",
                    _("You must type the same password each time."),
                )
        return self.cleaned_data

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        return user

    class Meta:
        model = get_user_model()
        fields = ['username']


class ChangeAvatarForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('avatar',)
