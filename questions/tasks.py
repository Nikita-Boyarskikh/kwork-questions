from celery import shared_task
from django.conf import settings
from django.db import transaction

from questions.models import Question, QuestionStatus, WrongStatusError


def change_question_status_task(question_id, status, next_task=None, countdown=0):
    with transaction.atomic():
        question = Question.objects.filter(id=question_id).select_for_update().first()
        if status not in question.allowed_status_transitions:
            raise WrongStatusError(from_status=question.status, to_status=status)
        question.status = status
        question.save()

        # TODO: send emails

        if next_task:
            task = next_task.apply_async(kwargs={
                'question_id': question_id,
            }, countdown=60 * 60 * countdown)
            return task.id


@shared_task
def publish_question(question_id):
    return change_question_status_task(
        question_id=question_id,
        status=QuestionStatus.PUBLISHED,
        next_task=close_answers,
        countdown=settings.CLOSE_ANSWERS_COUNTDOWN_HOURS,
    )


@shared_task
def close_answers(question_id):
    return change_question_status_task(
        question_id=question_id,
        status=QuestionStatus.ANSWERED,
        next_task=finish_voting,
        countdown=settings.FINISH_VOTING_COUNTDOWN_HOURS,
    )


@shared_task
def finish_voting(question_id):
    return change_question_status_task(
        question_id=question_id,
        status=QuestionStatus.CLOSED,
    )
