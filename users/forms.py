from captcha.fields import CaptchaField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from django.utils.translation import gettext as _


class AvatarFormMixin:
    @staticmethod
    def _validate_avatar_dimensions(w, h, max_width=1000, max_height=1000):
        if w > max_width or h > max_height:
            raise ValidationError({
                'avatar': _('Please use an image that is %(max_width)s x %(max_height)s pixels or smaller.') % {
                    'max_width': max_width,
                    'max_height': max_height,
                },
            })

    @staticmethod
    def _validate_avatar_content_type(content_type):
        main, sub = content_type.split('/')
        if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
            raise ValidationError({'avatar': _('Please use a JPEG, GIF or PNG image.')})

    @staticmethod
    def _validate_avatar_size(size, max_size=20 * 1024):
        if size > max_size:
            raise ValidationError({'avatar': _('Avatar file size may not exceed 20k.')})

    def _clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if avatar:
            w, h = get_image_dimensions(avatar)
            self._validate_avatar_dimensions(w, h)
            self._validate_avatar_content_type(avatar.content_type)


class SignupForm(AvatarFormMixin, ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = get_user_model()
        fields = ['pin', 'country', 'birth_year', 'sex', 'avatar', 'preferred_language']

    def signup(self, request, user):
        pass

    def clean(self):
        self._clean_avatar()
