from functools import partial

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView

from answers.models import Answer
from likes.models import Like, Subscription, LikeScore
from utils.views import CurrentCountryListViewMixin, MyListViewMixin


class ForScoreMixin:
    score = None

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(score=self.score)


class ForAnswerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            liked_object_content_type=Answer.content_type,
            liked_object_id=self.kwargs['answer_id'],
        )


class LikesListView(CurrentCountryListViewMixin, ForAnswerMixin, ForScoreMixin, ListView):
    score = LikeScore.LIKE
    model = Like
    template_name = 'likes/list.html'
    country_field_name = 'liked_object__country_id'


class DislikesListView(LikesListView):
    score = LikeScore.DISLIKE


class SubscriptionsListView(MyListViewMixin, ListView):
    model = Subscription
    template_name = 'questions/list.html'
    owner_field_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['object_list'] = [subscription.question for subscription in context['object_list']]
        return context


@login_required
def toggle_subscription(request, country_id, question_id):
    s, created = Subscription.objects.get_or_create(user=request.user, question_id=question_id)
    if not created:
        s.delete()
    return redirect('questions:index', country_id=country_id)


@transaction.atomic
@login_required
def change_reaction_score(request, target, country_id, answer_id):
    answer = Answer.objects.get(id=answer_id)
    if Like.is_voted_for_question(user=request.user, question=answer.question):
        messages.error(request, _('You already voted for this question'))
        return redirect('answers:index', country_id=country_id, question_id=answer.question_id)

    obj = Like.objects.create(
        user=request.user,
        score=target,
        liked_object_id=answer_id,
        liked_object_content_type=Answer.content_type,
    )
    return redirect(obj.liked_object)


like = partial(change_reaction_score, target=LikeScore.LIKE)
dislike = partial(change_reaction_score, target=LikeScore.DISLIKE)
likes = LikesListView.as_view()
dislikes = DislikesListView.as_view()
subscriptions = SubscriptionsListView.as_view()
