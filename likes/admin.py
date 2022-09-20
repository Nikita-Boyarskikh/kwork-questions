from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from likes.models import Like, Subscription
from utils.admin import ChangingDeniedMixin, AddingDeniedMixin, DeletingDeniedMixin


# TODO: make it editable by admin
class BaseLikeAdmin(AddingDeniedMixin, ChangingDeniedMixin, DeletingDeniedMixin):
    pass


class LikeInline(BaseLikeAdmin, GenericTabularInline):
    model = Like
    ct_field = 'liked_object_content_type'
    ct_fk_field = 'liked_object_id'
    extra = 0


class LikeAdmin(BaseLikeAdmin, admin.ModelAdmin):
    list_display = ('__str__', 'user', 'score_name', 'liked_object')
    search_fields = ('user', 'liked_object')
    list_filter = (
        ('score',)
    )


admin.site.register(Like, LikeAdmin)
admin.site.register(Subscription)
