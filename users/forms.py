from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from django.forms import ModelForm


# TODO: make preferred_language default with session.language_id or session.country_id
class SignupForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = get_user_model()
        fields = ('pin', 'country', 'birth_year', 'sex', 'avatar', 'preferred_language')

    def signup(self, request, user):
        pass


class ChangeAvatarForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('avatar',)
