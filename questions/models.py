from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.functional import classproperty
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel

from likes.models import Like, LikableModelMixin
from utils.generic_fields import WithSelfContentTypeMixin


class WrongStatusError(ValidationError):
    def __init__(self, from_status=None, to_status=None):
        message_parts = ['Impossible transition']
        if from_status:
            message_parts.append(f'from {from_status}')
        if to_status:
            message_parts.append(f'to {to_status}')
        super().__init__({
            'status': ' '.join(message_parts),
        })


class QuestionStatus(models.TextChoices):
    DRAFT = 'draft', _('In progress')  # -> pending
    DEFERRED = 'deferred', _('Deferred')  # -> pending
    PENDING = 'pending', _('Moderation')  # -> deferred/approved/rejected
    APPROVED = 'approved', _('Ready for publication')  # -> published
    REJECTED = 'rejected', _('Refused')
    PUBLISHED = 'published', _('Open')  # -> answered
    ANSWERED = 'answered', _('Voting')  # -> closed
    CLOSED = 'closed', _('Closed')

    @classproperty
    def transitions(cls):
        return {
            QuestionStatus.DRAFT: {QuestionStatus.PENDING},
            QuestionStatus.DEFERRED: {QuestionStatus.PENDING},
            QuestionStatus.PENDING: {QuestionStatus.DEFERRED, QuestionStatus.APPROVED, QuestionStatus.REJECTED},
            QuestionStatus.APPROVED: {QuestionStatus.PUBLISHED},
            QuestionStatus.REJECTED: set(),
            QuestionStatus.PUBLISHED: {QuestionStatus.ANSWERED},
            QuestionStatus.ANSWERED: {QuestionStatus.CLOSED},
            QuestionStatus.CLOSED: set(),
        }


class Question(TimeStampedModel, LikableModelMixin, WithSelfContentTypeMixin):
    _title_tr = _('Title').lower()
    _text_tr = _('Text').lower()
    _original_tr = _('Original')
    _translated_tr = _('Translated to english')

    status = models.CharField(_('Status'), max_length=100, choices=QuestionStatus.choices, default=QuestionStatus.DRAFT)
    status_changed = MonitorField(monitor='status')
    reason = models.TextField(_('Rejected reason'), blank=True)
    original_title = models.CharField(_original_tr + ' ' + _title_tr, max_length=80)
    en_title = models.CharField(_translated_tr + ' ' + _title_tr, max_length=80)
    original_text = models.TextField(_original_tr + ' ' + _text_tr)
    en_text = models.TextField(_translated_tr + ' ' + _text_tr)
    price = MoneyField(_('Price'), max_digits=14, default=settings.MIN_QUESTION_PRICE, validators=(
        MinMoneyValidator(settings.MIN_QUESTION_PRICE),
    ))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    best_answer = models.OneToOneField(
        'answers.Answer',
        related_name='best_for_question',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    language = models.ForeignKey('languages.Language', on_delete=models.SET(settings.DEFAULT_LANGUAGE))
    country = models.ForeignKey('countries.Country', on_delete=models.CASCADE)

    @property
    def allowed_status_transitions(self):
        return QuestionStatus.transitions[self.status]

    @property
    @admin.display(
        ordering='en_text',
        description=_('Truncated %s') % en_text.verbose_name.lower(),
    )
    def truncated_en_text(self):
        return Truncator(self.en_text).chars(20)

    # TODO
    def _clean_status(self, prev_status=None):
        return not prev_status \
               or self.status == prev_status \
               or self.status in QuestionStatus.transitions[prev_status]

    def _clean_best_answer(self):
        return not self.best_answer \
               or self.status == QuestionStatus.CLOSED \
               or self.best_answer.question == self

    def clean(self):
        errors = {}
        if not self._clean_status():
            transitions_map_str = '\n'.join(
                f'{start} -> {"/".join(targets or "x")}'
                for start, targets in QuestionStatus.transitions.items()
            )
            errors['status'] = _(
                'This status transition is not allowed\n'
                'Allowed transitions:\n%s'
            ) % transitions_map_str
        if not self._clean_best_answer():
            errors['best_answer'] = _('You should wait for question to be closed to select the best answer')

        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('answers:index', kwargs={
            'question_id': self.id,
            'country_id': self.country_id,
        })

    def __str__(self):
        return _('Question by %(author)s for %(country)s (%(price)s) - %(status)s') % {
            'author': self.author,
            'country': self.country,
            'price': self.price,
            'status': self.status,
        }

    class Meta:
        ordering = ('-price',)
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


# TODO: move to separate app and make it generic
class Comment(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    comment = models.TextField(_('Comment'))

    def __str__(self):
        return _('Comment by %(username)s for %(question_id)s: %(comment)s') % {
            'username': self.user.username,
            'question_id': self.question_id,
            'comment': self.comment,
        }

    class Meta:
        unique_together = [('question', 'user')]
        ordering = ('-created',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
