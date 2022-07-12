from django.contrib import admin

from languages.models import Language


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'yandex_id')
    search_fields = ('name', 'id', 'yandex_id')


admin.site.register(Language, LanguageAdmin)
