from annoying.functions import get_object_or_None
from constance import config
from django.db import models
from django.core.cache import cache
from django.urls import reverse
from django.utils.functional import classproperty
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

    @staticmethod
    def get_for_request(request):
        country_id = request.resolver_match.kwargs.get('country_id')

        if not country_id:
            if request.user.is_authenticated and request.user.country_id:
                country_id = request.user.country_id
            else:
                country_id = request.session.get('country_id')

        if country_id and country_id != 'unknown':
            request.session['country_id'] = country_id
            if request.user.is_authenticated:
                request.user.country_id = country_id
                request.user.save()
            return get_object_or_None(Country.objects.filter(id=country_id))

    @classproperty
    def default(cls):
        default_country = cache.get('default_country')
        if default_country:
            return default_country

        default_country = cls.objects.get(pk=config.DEFAULT_COUNTRY)
        cache.set('default_country', default_country)
        return default_country

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('name',)
