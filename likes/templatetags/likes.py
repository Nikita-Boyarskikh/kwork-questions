from django import template

register = template.Library()


@register.filter
def liked_by_me(obj, request):
    if not request.user.is_authenticated:
        return False
    return obj.likes.filter(user=request.user).exists()
