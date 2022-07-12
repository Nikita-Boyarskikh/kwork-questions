from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Country(models.Model):
    id = models.CharField(_('Code'), primary_key=True, max_length=255)
    name = models.CharField(_('Name'), max_length=255)
    language = models.ForeignKey('languages.Language', on_delete=models.RESTRICT)
    population = models.IntegerField(_('Population'), blank=True, null=True)
    live_quality_index = models.IntegerField(
        _('Live quality index'),
        blank=True,
        null=True,
        help_text=_('Taken from numbeo.com'),
    )

    def clean(self):
        if not self.name:
            self.name = self.id.capitalize()

    def get_absolute_url(self):
        return reverse('countries:details', args=[self.pk])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
