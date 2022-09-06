from django import template

from project.settings import USDT

register = template.Library()


@register.filter
def is_current_url(request, url_name):
    return request.path_info == url_name


@register.filter
def split(value, divider=' '):
    return value.split(divider)


@register.filter
def currency_icon(currency):
    return {
        USDT: 'icons/usdt.png',
    }[currency]
