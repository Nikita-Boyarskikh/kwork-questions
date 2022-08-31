from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.db.models import Q, Count
from django.utils.timezone import now

from accounts.models import AccountAction, AccountActionType, AccountActionStatus
from lib.celery import app
from likes.models import LikeScore
from questions.models import Question, QuestionStatus, WrongStatusError


def change_question_status_task(question, status, next_task=None, countdown=0):
    if status not in question.allowed_status_transitions:
        raise WrongStatusError(from_status=question.status, to_status=status)
    question.status = status
    question.save()

    # TODO: send emails

    if next_task:
        task = next_task.apply_async(kwargs={
            'question_id': question.id,
        }, countdown=60 * 60 * countdown)
        return task.id


@app.task
def publish_questions():
    with transaction.atomic():
        yesterday = now() - timedelta(days=1)
        for question in Question.objects.select_for_update().filter(
            Q(status=QuestionStatus.APPROVED)
            | Q(status=QuestionStatus.PENDING, status_changed__gte=yesterday)
        ).all():
            if question.status == QuestionStatus.PENDING:
                question.status = QuestionStatus.APPROVED
            change_question_status_task(
                question=question,
                status=QuestionStatus.PUBLISHED,
                next_task=close_answers,
                countdown=settings.CLOSE_ANSWERS_COUNTDOWN_HOURS,
            )


@shared_task
def close_answers(question_id):
    with transaction.atomic():
        question = Question.objects.select_for_update().get(id=question_id)
        change_question_status_task(
            question=question,
            status=QuestionStatus.ANSWERED,
            next_task=finish_voting,
            countdown=settings.FINISH_VOTING_COUNTDOWN_HOURS,
        )


@shared_task
def finish_voting(question_id):
    with transaction.atomic():
        question = Question.objects.select_for_update().get(id=question_id)

        question.best_answer = question.answer_set\
            .filter(reactions__score=LikeScore.LIKE)\
            .annotate(Count('reactions'))\
            .order_by('-reactions__count', 'reactions__created')\
            .first()

        if question.best_answer:
            AccountAction.objects.create(
                account=question.best_answer.author.account,
                type=AccountActionType.GET_AWARD,
                delta=settings.ANSWER_REWARD_PRICE,
                status=AccountActionStatus.APPROVED,
                product=question.best_answer,
            )

        change_question_status_task(
            question=question,
            status=QuestionStatus.CLOSED,
        )
