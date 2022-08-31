from annoying.functions import get_object_or_this
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.functional import classproperty
from django.utils.translation import gettext as _, get_language_from_request


class Language(models.Model):
    id = models.CharField(_('Code'), primary_key=True, max_length=255)
    name = models.CharField(_('Name'), max_length=255)
    google_id = models.CharField(
        _('Google.Translate id'),
        help_text=_('ID for use as an argument for Google.Translate API'),
        max_length=2,
    )

    def clean(self):
        if not self.name:
            self.name = self.id.capitalize()

    def __str__(self):
        return self.name

    @classproperty
    def default(cls):
        default_language = cache.get('default_language')
        if default_language:
            return default_language

        default_language = cls.objects.get(pk=settings.DEFAULT_LANGUAGE)
        cache.set('default_language', default_language)
        return default_language

    @classmethod
    def get_for_request(cls, request):
        if request.user.is_authenticated and request.user.preferred_language:
            return request.user.preferred_language
        current_language_code, *subcodes = get_language_from_request(request).split('-')
        return get_object_or_this(cls, cls.default, pk=current_language_code)

    class Meta:
        ordering = ('-name',)
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
