from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from likes.models import Like, Subscription


class LikeInline(GenericTabularInline):
    model = Like
    ct_field = 'liked_object_content_type'
    ct_fk_field = 'liked_object_id'
    extra = 0


class LikeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'score_name', 'liked_object')
    search_fields = ('author', 'comment', 'liked_object')
    list_filter = (
        ('score',)
    )
    readonly_fields = ('created', 'modified')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Like, LikeAdmin)
admin.site.register(Subscription)
