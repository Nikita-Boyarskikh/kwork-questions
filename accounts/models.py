import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import classproperty
from django.utils.translation import gettext as _
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from model_utils.models import TimeStampedModel

from accounts.utils import zero_money
from accounts.validators import not_zero_money_validator
from utils.generic_fields import content_type_limit_choices_by_model_references, IntegerForAutoField


class AccountActionType(models.TextChoices):
    PAY_SERVICE_FEE = 'pay_service_fee'
    GET_AWARD = 'get_award'
    WITHDRAW = 'withdraw'
    DEPOSIT = 'deposit'
    OTHER = 'other'


class AccountActionStatus(models.TextChoices):
    CREATED = 'created'
    APPROVED = 'approved'
    DECLINED = 'declined'

    # TODO
    @classproperty
    def transitions(cls):
        return {
            cls.CREATED: {cls.APPROVED, cls.DECLINED},
            cls.APPROVED: set(),
            cls.DECLINED: set(),
        }


class Account(TimeStampedModel):
    uid = models.UUIDField(_('Public identifier'), unique=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False)
    balance = MoneyField(_('Balance'), default=0, max_digits=14, validators=(
        MinMoneyValidator(0),
    ), editable=False)

    def __str__(self):
        return f'{self.user} ({self.balance})'

    class Meta:
        ordering = ('-user__date_joined',)
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')


class AccountAction(TimeStampedModel):
    PRODUCT_TYPES = ('questions.Question', 'answers.Answer')

    uid = models.UUIDField(_('Public identifier'), unique=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, editable=False)
    type = models.CharField(
        _('Type'),
        max_length=100,
        choices=AccountActionType.choices,
        default=AccountActionType.OTHER,
    )
    status = models.CharField(
        _('Status'),
        max_length=100,
        choices=AccountActionStatus.choices,
        default=AccountActionStatus.CREATED,
    )
    delta = MoneyField(_('Delta'), max_digits=14, validators=(not_zero_money_validator,), default=0)
    comment = models.TextField(_('Comment'), blank=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        limit_choices_to=content_type_limit_choices_by_model_references(PRODUCT_TYPES),
        null=True,
        blank=True,
    )
    object_id = IntegerForAutoField(_('Awarded/payed for question/answer id'), null=True, blank=True)
    product = GenericForeignKey()

    def __str__(self):
        for_product = _(' for %(product_type)s %(product_id)s') % {
            'product_type': self.content_type,
            'product_id': self.object_id,
        } if self.product else ''
        return f'{self.account.user} {self.type} {self.delta} ({self.status}){for_product}'

    def _clean_delta_type(self):
        negative_delta_types = {AccountActionType.PAY_SERVICE_FEE, AccountActionType.WITHDRAW, AccountActionType.OTHER}
        positive_delta_types = {AccountActionType.GET_AWARD, AccountActionType.DEPOSIT, AccountActionType.OTHER}
        zero = zero_money()
        return self.delta < zero and self.type in negative_delta_types \
            or self.delta > zero and self.type in positive_delta_types

    def _clean_delta(self):
        return self.delta + self.account.balance >= zero_money()

    def clean(self):
        from answers.models import Answer
        from questions.models import Question

        content_type_type_map = {
            Answer.content_type: AccountActionType.GET_AWARD,
            Question.content_type: AccountActionType.PAY_SERVICE_FEE,
        }
        errors = {}

        if not self._clean_delta():
            errors['delta'] = _('Insufficient funds on account')
        elif not self._clean_delta_type():
            errors['delta'] = _('Delta should corresponds with action type')

        required_type = content_type_type_map.get(self.content_type)
        if required_type and self.type != required_type.value:
            errors['type'] = _('Type should be %(type)s for %(content_type)s related action') % {
                'type': required_type,
                'content_type': self.content_type.name,
            }

        if errors:
            raise ValidationError(errors)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Account Action')
        verbose_name_plural = _('Account Actions')
