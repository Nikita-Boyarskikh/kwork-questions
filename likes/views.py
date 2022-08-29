from django.views.generic import ListView

from likes.models import Like, LikeScore
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


class MyLikesListView(LikesListView, MyListViewMixin):
    owner_field_name = 'user'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(score=LikeScore.LIKE)


index = LikesForObjectListView.as_view()
my = MyLikesListView.as_view()
