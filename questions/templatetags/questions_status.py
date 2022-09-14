from django import template

from questions.models import QuestionStatus

register = template.Library()


@register.filter
def question_status_class(question):
    return {
        QuestionStatus.DRAFT: 'warning',
        QuestionStatus.DEFERRED: 'warning',
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
        QuestionStatus.DRAFT: 'icons/band.png',
        QuestionStatus.DEFERRED: 'icons/band.png',
        QuestionStatus.PENDING: 'icons/clock.png',
        QuestionStatus.APPROVED: 'icons/checkmark.png',
        QuestionStatus.REJECTED: 'icons/cross.png',
        QuestionStatus.PUBLISHED: 'icons/clock.png',
        QuestionStatus.ANSWERED: 'icons/clock.png',
    }.get(question.status, 'icons/question.png')
