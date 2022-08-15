from django.contrib import admin

from languages.models import Language


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'google_id')
    search_fields = ('name', 'id', 'google_id')


admin.site.register(Language, LanguageAdmin)
