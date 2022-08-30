from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from utils.generic_fields import content_type_limit_choices_by_model_references, IntegerForAutoField


class LikeScore(models.IntegerChoices):
    LIKE = 1
    DISLIKE = -1


class Like(TimeStampedModel):
    CAN_LIKE = {'questions.Question', 'answers.Answer'}

    score = models.IntegerField(_('Like/dislike'), choices=LikeScore.choices, default=LikeScore.LIKE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    liked_object_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=content_type_limit_choices_by_model_references(CAN_LIKE),
    )
    liked_object_id = IntegerForAutoField(_('Liked/disliked question/answer id'))
    liked_object = GenericForeignKey('liked_object_content_type', 'liked_object_id')

    @classmethod
    def like(cls, user, disliked_object):
        return cls(score=LikeScore.LIKE, user=user, liked_object=disliked_object)

    @classmethod
    def dislike(cls, user, liked_object):
        return cls(score=LikeScore.DISLIKE, user=user, liked_object=liked_object)

    @property
    @admin.display(
        ordering='score',
        description=_('Score'),
    )
    def score_name(self):
        return LikeScore(self.score).name.lower()

    def _get_errors_for_liked_object(self):
        from questions.models import Question, QuestionStatus

        required_status = QuestionStatus.ANSWERED
        if self.liked_object_content_type == ContentType.objects.get_for_model(Question) \
                and not self.liked_object.status == required_status:
            return _('Question status should be %(status)') % required_status

    def _clean_user(self):
        return self.user != self.liked_object.author

    def clean(self):
        errors = {
            'liked_object_id': self._get_errors_for_liked_object()
        }

        if not self._clean_user():
            errors['user'] = _("%(liked_object_type)s's author can't like it") % {
                'liked_object_type': self.liked_object_content_type.name,
            }

        raise ValidationError(errors)

    def __str__(self):
        score = _('like') if self.score == LikeScore.LIKE else _('dislike')
        return f'{self.user} {score} {self.liked_object_content_type.name} {self.liked_object_id}'

    class Meta:
        ordering = ('-created',)
        unique_together = [('liked_object_content_type', 'liked_object_id', 'user')]
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')


class LikableModelMixin(models.Model):
    reactions = GenericRelation(Like, 'liked_object_id', 'liked_object_content_type')

    @property
    def likes(self):
        return self.reactions.filter(score=LikeScore.LIKE)

    @property
    def dislikes(self):
        return self.reactions.filter(score=LikeScore.DISLIKE)

    class Meta:
        abstract = True


class Subscription(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE)

    def __str__(self):
        return _('Subscription of %(username)s for %(question_id)') % {
            'username': self.user.username,
            'question_id': self.question_id,
        }

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
