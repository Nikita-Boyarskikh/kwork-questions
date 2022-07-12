from django.contrib import admin

from countries.models import Country


class CountryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'language', 'live_quality_index', 'population')
    search_fields = ('id', 'name')
    list_filter = ('live_quality_index', 'population')


admin.site.register(Country, CountryAdmin)
