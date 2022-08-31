from django import template

from likes.models import Like

register = template.Library()


@register.filter
def subscribed(obj, user):
    if not user.is_authenticated:
        return False
    return obj.subscription_set.filter(user=user).exists()


@register.filter
def liked_by_me(obj, me):
    if not me.is_authenticated:
        return False
    return obj.likes.filter(user=me).exists()


@register.filter
def disliked_by_me(obj, me):
    if not me.is_authenticated:
        return False
    return obj.dislikes.filter(user=me).exists()


@register.filter
def is_voted_for_question(question, me):
    return Like.is_voted_for_question(user=me, question=question)
