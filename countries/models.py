from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Country(models.Model):
    id = models.CharField(_('Code'), primary_key=True, max_length=255)
    name = models.CharField(_('Name'), max_length=255)
    language = models.ForeignKey('languages.Language', blank=True, null=True, on_delete=models.SET_NULL)
    population = models.IntegerField(_('Population'), blank=True, null=True)
    live_quality_index = models.IntegerField(
        _('Live quality index'),
        blank=True,
        null=True,
        help_text=_('From https://ru.wikipedia.org/wiki/Список_стран_по_индексу_человеческого_развития'),
    )

    def clean(self):
        if not self.name:
            self.name = self.id.capitalize()

    def get_absolute_url(self):
        return reverse('questions:index', kwargs={'country_id': self.id})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('name',)
