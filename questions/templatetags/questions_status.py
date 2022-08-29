from django import template

from questions.models import QuestionStatus

register = template.Library()


@register.filter
def question_status_class(question):
    return {
        QuestionStatus.DRAFT: 'warning',
        QuestionStatus.PENDING: 'info',
        QuestionStatus.APPROVED: 'success',
        QuestionStatus.REJECTED: 'danger',
        QuestionStatus.PUBLISHED: 'primary',
        QuestionStatus.ANSWERED: 'primary',
        QuestionStatus.CLOSED: 'secondary',
    }[question.status]


@register.filter
def question_status_icon(question):
    return {
        QuestionStatus.DRAFT: 'exclamation-circle',
        QuestionStatus.PENDING: 'clock',
        QuestionStatus.APPROVED: 'check-circle',
        QuestionStatus.REJECTED: 'x-circle',
        QuestionStatus.PUBLISHED: 'clock',
        QuestionStatus.ANSWERED: 'clock',
        QuestionStatus.CLOSED: 'slash-circle',
    }[question.status]
