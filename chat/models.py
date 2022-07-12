from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel


class Message(TimeStampedModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='outbox_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='inbox_messages', on_delete=models.CASCADE)
    is_read = models.BooleanField(_('Is read?'), default=False)
    content = models.TextField(_('Content'))
    subject = models.CharField(_('Subject'), max_length=255)

    @property
    @admin.display(
        ordering='content',
        description=_('Truncated %s') % content.verbose_name.lower(),
    )
    def truncated_content(self):
        return Truncator(self.content).chars(20)

    @property
    @admin.display(
        ordering='subject',
        description=_('Truncated %s') % subject.verbose_name.lower(),
    )
    def truncated_subject(self):
        return Truncator(self.subject).chars(10)

    def _clean_sender_and_recipient_different(self):
        return self.sender != self.recipient

    def _clean_only_is_staff_chat(self):
        return self.sender.is_staff or self.recipient.is_staff

    def clean(self):
        errors = {}

        if not self._clean_sender_and_recipient_different():
            errors['sender'] = errors['recipient'] = _('Sender and recipient should differs')
        elif not self._clean_only_is_staff_chat():
            errors['sender'] = errors['recipient'] = _('Sender or recipient should be staff user')

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return _('Message from %(sender)s to %(recipient)s: %(subject)s') % {
            'sender': self.sender,
            'recipient': self.recipient,
            'subject': self.truncated_subject,
        }

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
