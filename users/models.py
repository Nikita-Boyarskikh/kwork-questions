from allauth.account.models import EmailAddress
from allauth.account.utils import user_email
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext as _

from accounts.models import Account
from users.auth import AccountAdapter, send_email_confirmation
from users.validators import max_value_current_year_validator


class Education(models.TextChoices):
    ASSOCIATE = 'associate'
    BACHELOR = 'bachelor'
    MASTER = 'master'
    DOCTOR = 'doctor'

    __empty__ = _('Without education')


class Sex(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'

    __empty__ = _('Prefer not to say / unsure')


def _build_avatar_filename(user):
    return f'avatars/{user.username}'


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        with transaction.atomic():
            user = super().create_user(username, email, password, **extra_fields)
            send_email_confirmation(user)
            Account.objects.create(user=user)
            return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        with transaction.atomic():
            user = super().create_superuser(username, email, password, **extra_fields)
            send_email_confirmation(user)
            Account.objects.create(user=user)
            return user


class User(AbstractUser):
    avatar = models.ImageField(_('Avatar'), upload_to=_build_avatar_filename, blank=True, null=True)
    email = models.EmailField(_('email address'))
    first_name = None
    last_name = None
    is_approved = models.BooleanField(
        _('Approved'),
        default=False,
        help_text=_('User approved with control question.'),
    )
    is_user_agreement_accepted = models.BooleanField(
        _('User agreement accepted'),
        default=False,
        help_text=_('User can create a question only after accept a user agreement.'),
    )
    pin = models.CharField(_('Pin'), max_length=128)
    country = models.ForeignKey('countries.Country', on_delete=models.SET_NULL, blank=True, null=True)
    preferred_language = models.ForeignKey('languages.Language', on_delete=models.SET(settings.DEFAULT_LANGUAGE))
    sex = models.CharField(_('Sex'), max_length=10, choices=Sex.choices, null=True, blank=True)
    education = models.CharField(_('Education'), max_length=10, choices=Education.choices, null=True, blank=True)
    birth_year = models.PositiveIntegerField(
        _('Birth year'),
        validators=[MinValueValidator(1900), max_value_current_year_validator],
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ['email', 'pin', 'preferred_language_id']

    objects = UserManager()

    def clean(self):
        AccountAdapter().validate_unique_email(self.email)

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
