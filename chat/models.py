from collections import defaultdict

from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel


class Message(TimeStampedModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='outbox_messages', on_delete=models.CASCADE, editable=False)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inbox_messages', on_delete=models.CASCADE, editable=False)
    is_read = models.BooleanField(_('Is read?'), default=False)
    content = models.TextField(_('Content'))

    @property
    @admin.display(
        ordering='content',
        description=_('Truncated %s') % content.verbose_name.lower(),
    )
    def truncated_content(self):
        return Truncator(self.content).chars(20)

    def _clean_sender_and_recipient_different(self):
        return self.sender != self.recipient

    def _clean_only_is_staff_chat(self):
        return self.sender.is_staff or self.recipient.is_staff

    def clean(self):
        errors = defaultdict(list)

        if not self._clean_sender_and_recipient_different():
            errors[NON_FIELD_ERRORS].append(_('Sender and recipient should differs'))
        elif not self._clean_only_is_staff_chat():
            errors[NON_FIELD_ERRORS].append(_('Sender or recipient should be staff user'))

        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('chat:index')

    def __str__(self):
        return _('Message from %(sender)s to %(recipient)s: %(content)s') % {
            'sender': self.sender,
            'recipient': self.recipient,
            'content': self.truncated_content,
        }

    class Meta:
        ordering = ('created',)
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
