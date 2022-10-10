from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from django.forms import ModelForm


class SignupForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = get_user_model()
        fields = []

    def signup(self, request, user):
        pass


class ChangeAvatarForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('avatar',)
