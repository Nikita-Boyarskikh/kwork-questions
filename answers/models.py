from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from accounts.models import AccountAction
from claims.models import Claim
from likes.models import Like
from questions.models import QuestionStatus


class Answer(TimeStampedModel):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    original_text = models.TextField(_('Original text'))
    en_text = models.TextField(_('Translated to english text'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.SET(settings.DEFAULT_LANGUAGE))
    likes = GenericRelation(Like, 'liked_object_id', 'liked_object_content_type')
    claims = GenericRelation(Claim)
    account_actions = GenericRelation(AccountAction)
    views = models.PositiveIntegerField(_('Views'), default=0)

    @property
    @admin.display(
        ordering='question__status',
        description=_('Question') + ' ' + _('Status').lower(),
    )
    def question__status(self):
        return self.question.status

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
        return Truncator(self.en_text).chars(20)

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
        errors = {}

        if not self._clean_author():
            errors['author'] = _("Question's author can't answer to it")
        elif not self._clean_question_status():
            errors['question'] = _('Question status should be %s') % QuestionStatus.PUBLISHED

        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('answers:details', args=[self.pk])

    class Meta:
        ordering = ('-created',)
        unique_together = [('question', 'author')]
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
