from django import template

register = template.Library()


@register.filter
def subscribed(obj, request):
    if not request.user.is_authenticated:
        return False
    return obj.subscription_set.filter(user=request.user).exists()


@register.filter
def liked_by_me(obj, request):
    if not request.user.is_authenticated:
        return False
    return obj.likes.filter(user=request.user).exists()


@register.filter
def disliked_by_me(obj, request):
    if not request.user.is_authenticated:
        return False
    return obj.dislikes.filter(user=request.user).exists()
