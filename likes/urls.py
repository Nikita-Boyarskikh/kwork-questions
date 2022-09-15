from django.urls import path, include

from likes.views import subscriptions, likes, dislikes, toggle_subscription, like, dislike

app_name = 'likes'
urlpatterns = [
    path('<str:content_type>/<int:object_id>/', include([
        path('likes', likes, name='likes'),
        path('dislikes', dislikes, name='dislikes'),
        path('like', like, name='like'),
        path('dislike', dislike, name='dislike'),
    ])),
    path('subscriptions', subscriptions, name='subscriptions'),
    path('<int:question_id>/toggle_subscription', toggle_subscription, name='toggle_subscription'),
]
