from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from claims.models import Claim


class ClaimInline(GenericTabularInline):
    model = Claim
    extra = 0


class ClaimAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'claimed_object', 'truncated_comment')
    search_fields = ('author', 'comment', 'claimed_object__en_text', 'claimed_object__original_text')


admin.site.register(Claim, ClaimAdmin)
