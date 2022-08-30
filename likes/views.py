from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import ListView

from likes.models import Like, Subscription
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


index = LikesForObjectListView.as_view()
my = MySubscriptionsListView.as_view()
