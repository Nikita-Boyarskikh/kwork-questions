from allauth.account.models import EmailAddress
from constance import config
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext as _

from accounts.models import Account
from users.auth import AccountAdapter
from users.validators import avatar_validator


def _build_avatar_filename(user, filename):
    return f'avatars/{user.username}/{filename}'


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        with transaction.atomic():
            user = super().create_user(username, email, password, **extra_fields)
            Account.objects.create(user=user)
            return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        with transaction.atomic():
            user = super().create_superuser(username, email, password, **extra_fields)
            Account.objects.create(user=user)
            return user


class User(AbstractUser):
    def __init__(self, *args, email=None, **kwargs):
        return super().__init__(*args, **kwargs)

    avatar = models.ImageField(
        _('Avatar'),
        upload_to=_build_avatar_filename,
        blank=True,
        null=True,
        validators=[avatar_validator],
    )
    email = None
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
    country = models.ForeignKey('countries.Country', default=config.DEFAULT_COUNTRY, on_delete=models.SET_DEFAULT)
    preferred_language = models.ForeignKey('languages.Language', default=config.DEFAULT_LANGUAGE, on_delete=models.SET_DEFAULT)

    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')
