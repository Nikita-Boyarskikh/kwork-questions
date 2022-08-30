from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import ListView

from likes.models import Like, Subscription, LikeScore
from questions.models import Question
from utils.views import CurrentCountryListViewMixin, MyListViewMixin


class LikesListView(ListView, CurrentCountryListViewMixin):
    model = Like
    template_name = 'likes/list.html'
    country_field_name = 'liked_object__country_id'


class LikesForObjectListView(LikesListView):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            liked_object_content_type=self.kwargs['content_type'],
            liked_object_id=self.kwargs['object_id'],
        )


class MySubscriptionsListView(ListView, MyListViewMixin):
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
def like(request, country_id, question_id):
    question_content_type = ContentType.objects.get_for_model(Question)
    try:
        obj = Like.objects.select_for_update().get(
            user=request.user,
            liked_object_id=question_id,
            liked_object_content_type=question_content_type,
        )
        if obj.score == LikeScore.DISLIKE:
            obj.score = LikeScore.LIKE
            obj.save()
        else:
            obj.delete()
    except Like.DoesNotExist:
        obj = Like.like(
            user=request.user,
            object_id=question_id,
            object_content_type=question_content_type,
        )
        obj.save()
    return redirect(obj.liked_object)


@transaction.atomic
@login_required
def dislike(request, country_id, question_id):
    question_content_type = ContentType.objects.get_for_model(Question)
    try:
        obj = Like.objects.select_for_update().get(
            user=request.user,
            liked_object_id=question_id,
            liked_object_content_type=question_content_type,
        )
        if obj.score == LikeScore.LIKE:
            obj.score = LikeScore.DISLIKE
            obj.save()
        else:
            obj.delete()
    except Like.DoesNotExist:
        obj = Like.dislike(
            user=request.user,
            object_id=question_id,
            object_content_type=question_content_type,
        )
        obj.save()
    return redirect(obj.liked_object)


index = LikesForObjectListView.as_view()
my = MySubscriptionsListView.as_view()
