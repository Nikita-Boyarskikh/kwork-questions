from functools import partial

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import BadRequest
from django.db import transaction
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView

from answers.models import Answer
from likes.models import Like, Subscription, LikeScore
from questions.models import Question
from utils.views import MyListViewMixin, ForGenericMixin


class ForScoreMixin:
    score = None

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(score=self.score)


class LikesListView(ForGenericMixin, ForScoreMixin, ListView):
    content_type_field = 'liked_object_content_type'
    object_id_field = 'liked_object_id'
    score = LikeScore.LIKE
    model = Like
    template_name = 'likes/list.html'
    country_field_name = 'liked_object__country_id'

    def get_queryset(self):
        qs = super().get_queryset()
        country_id = self.kwargs.get('country_id')
        if not country_id or country_id == 'unknown':
            return qs
        return [l for l in qs if l.liked_object.question.country_id == country_id]


class DislikesListView(LikesListView):
    score = LikeScore.DISLIKE


class SubscriptionsListView(MyListViewMixin, ListView):
    model = Subscription
    template_name = 'questions/list.html'
    owner_field_name = 'user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['object_list'] = [subscription.question for subscription in context['object_list']]
        context['url_name'] = 'likes:subscriptions'
        return context


@login_required
def toggle_subscription(request, country_id, question_id):
    s, created = Subscription.objects.get_or_create(user=request.user, question_id=question_id)
    if not created:
        s.delete()
    return redirect('questions:index', country_id=country_id)


@transaction.atomic
@login_required
def change_reaction_score(request, target, country_id, content_type, object_id):
    already_voted_message = _('You already voted for this question')

    if content_type == 'answer':
        liked_object = Answer.objects.get(id=object_id)
        if Like.is_voted_for_question(user=request.user, question=liked_object.question):
            messages.error(request, already_voted_message)
            return redirect('answers:index', country_id=country_id, question_id=liked_object.question_id)

    elif content_type == 'question':
        liked_object = Question.objects.get(id=object_id)
        if liked_object.likes.filter(user=request.user).exists():
            messages.error(request, already_voted_message)
            return redirect('answers:index', country_id=country_id, question_id=liked_object.id)
    else:
        raise BadRequest()

    Like.objects.create(
        user=request.user,
        score=target,
        liked_object=liked_object,
    )
    return redirect(liked_object)


like = partial(change_reaction_score, target=LikeScore.LIKE)
dislike = partial(change_reaction_score, target=LikeScore.DISLIKE)
likes = LikesListView.as_view()
dislikes = DislikesListView.as_view()
subscriptions = SubscriptionsListView.as_view()
