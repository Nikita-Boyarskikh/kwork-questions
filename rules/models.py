from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class Rule(models.Model):
    content = models.TextField(_('Rule text'))
    language = models.ForeignKey('languages.Language', default=settings.DEFAULT_LANGUAGE, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _('Rule')
        verbose_name_plural = _('Rules')
