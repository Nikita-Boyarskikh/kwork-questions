from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

from utils.generic_fields import content_type_limit_choices_by_model_references, IntegerForAutoField


class Claim(TimeStampedModel):
    OBJECT_TYPES = {'answers.Answer'}

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(_('Comment'), blank=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=content_type_limit_choices_by_model_references(OBJECT_TYPES), null=True, blank=True,
    )
    object_id = IntegerForAutoField(_('Claimed answer id'), null=True, blank=True)
    claimed_object = GenericForeignKey()

    @property
    @admin.display(
        ordering='comment',
        description=_('Truncated %s') % comment.verbose_name.lower(),
    )
    def truncated_comment(self):
        return Truncator(self.comment).chars(20)

    def _clean_author(self):
        claimed_object = self.content_type.get_object_for_this_type(pk=self.object_id)
        return self.author != claimed_object.author

    def clean(self):
        errors = {}

        if not self._clean_author():
            errors['author'] = _("User can't claim for his own %(content_type)s") % {
                'content_type': self.content_type.name,
            }

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return _('Claim for %(content_type)s %(object_id)s by %(author)s') % {
            'content_type': self.content_type.name,
            'object_id': self.object_id,
            'author': self.author,
        }

    class Meta:
        ordering = ('-created',)
        unique_together = [('content_type', 'object_id', 'author')]
        verbose_name = _('Claim')
        verbose_name_plural = _('Claims')
