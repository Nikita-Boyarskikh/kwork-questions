from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def is_current_url(request, url_name):
    return request.path_info == url_name


@register.filter
def split(value, divider=' '):
    return value.split(divider)


@register.filter
def content_type(obj):
    return ContentType.objects.get_for_model(obj).id
