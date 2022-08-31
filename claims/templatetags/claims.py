from django import template

from answers.models import Answer
from claims.models import Claim

register = template.Library()


@register.filter
def is_claimed_by_me(answer, me):
    return Claim.objects.filter(content_type=Answer.content_type, object_id=answer.id, author=me).exists()

