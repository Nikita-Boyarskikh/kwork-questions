from collections import defaultdict

from constance import config
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from accounts.models import AccountAction
from claims.models import Claim
from likes.models import Like, LikableModelMixin
from questions.models import QuestionStatus
from utils.generic_fields import WithSelfContentTypeMixin


class Answer(TimeStampedModel, LikableModelMixin, WithSelfContentTypeMixin):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, editable=False)
    original_text = models.TextField(_('Original text'))
    en_text = models.TextField(_('Translated to english text'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    language = models.ForeignKey('languages.Language', on_delete=models.SET(config.DEFAULT_LANGUAGE))
    claims = GenericRelation(Claim)

    @property
    @admin.display(
        ordering='question__status',
        description=_('Question') + ' ' + _('Status').lower(),
    )
    def question__status(self):
        return QuestionStatus(self.question.status)

    @property
    @admin.display(
        ordering='views',
        description=_('Answer') + ' ' + _('Views').lower() + ' ' + _('Count').lower(),
    )
    def views__count(self):
        return self.answerview_set.count()

    @property
    @admin.display(
        ordering='question__country',
        description=_('Question') + ' ' + _('Country').lower(),
    )
    def question__country(self):
        return self.question.country

    @property
    @admin.display(
        ordering='en_text',
        description=_('Truncated %s') % en_text.verbose_name.lower(),
    )
    def truncated_en_text(self):
        return Truncator(self.en_text).chars(config.ANSWER_PREVIEW_TEXT_SIZE)

    def __str__(self):
        return _('Answer for Question %(question_id)s by %(author)s') % {
            'question_id': self.question.id,
            'author': self.author,
        }

    def _clean_question_status(self):
        return self.question.status == QuestionStatus.PUBLISHED

    def _clean_author(self):
        return self.author != self.question.author

    def clean(self):
        errors = defaultdict(list)

        if not self._clean_author():
            errors[NON_FIELD_ERRORS].append(
                ValidationError(
                    message=_("Question's author can't answer to it"),
                    code='same_question_author',
                )
            )
        elif not self._clean_question_status():
            errors[NON_FIELD_ERRORS].append(
                ValidationError(
                    message=_('Question status should be %(status)s'),
                    params={
                        'status': QuestionStatus.PUBLISHED,
                    },
                    code='wrong_question_status',
                )
            )

        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('answers:index', kwargs={
            'country_id': self.question__country.id,
            'question_id': self.question_id,
        })

    class Meta:
        ordering = ('-created',)
        unique_together = [('question', 'author')]
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')


# TODO: move to separate app and make it generic
class AnswerView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT, editable=False)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return _('Answer view for %(answer_id)s by %(username)s') % {
            'answer_id': self.answer_id,
            'username': self.user.username
        }

    class Meta:
        ordering = ('-answer__created',)
        unique_together = [('answer', 'user')]
        verbose_name = _('Answer view')
        verbose_name_plural = _('Answer views')
