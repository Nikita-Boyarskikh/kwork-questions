from django import template


register = template.Library()


@register.filter
def is_not_answered_by_me(question, me):
    return not question.answer_set.filter(author=me).exists()
