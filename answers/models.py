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
from likes.models import Like, LikableModelMixin
from questions.models import QuestionStatus


class Answer(TimeStampedModel, LikableModelMixin):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)
    original_text = models.TextField(_('Original text'))
    en_text = models.TextField(_('Translated to english text'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.ForeignKey('languages.Language', on_delete=models.SET(settings.DEFAULT_LANGUAGE))
    claims = GenericRelation(Claim)
    account_actions = GenericRelation(AccountAction)

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
        return self.answerviews_set.count()

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
        return Truncator(self.en_text).chars(settings.ANSWER_PREVIEW_TEXT_SIZE)

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
        return reverse('answers:detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ('-created',)
        unique_together = [('question', 'author')]
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')


class AnswerViews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return _('Answer view for %(answer_id)s by %(user)s')

    class Meta:
        unique_together = [('answer', 'user')]
        verbose_name = _('Answer view')
        verbose_name_plural = _('Answer views')
