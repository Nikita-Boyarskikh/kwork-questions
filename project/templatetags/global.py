from django import template

register = template.Library()


@register.filter
def is_current_url(request, url_name):
    return request.path_info == url_name


@register.filter
def split(value, divider=' '):
    return value.split(divider)
