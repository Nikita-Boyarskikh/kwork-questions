from django import template


register = template.Library()


@register.filter
def is_answered_by_me(question, me):
    return question.answer_set.filter(author=me).exists()
