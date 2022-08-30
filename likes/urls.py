from django.urls import path

from likes.views import my, index, toggle_subscription, like, dislike

app_name = 'likes'
urlpatterns = [
    path('<str:content_type>/<int:object_id>', index, name='index'),
    path('my', my, name='my'),
    path('<int:question_id>/toggle_subscription', toggle_subscription, name='toggle_subscription'),
    path('<int:question_id>/like', like, name='like'),
    path('<int:question_id>/dislike', dislike, name='dislike'),
]
