from django.urls import path

from likes.views import my, index

app_name = 'likes'
urlpatterns = [
    path('<str:content_type>/<int:object_id>', index, name='index'),
    path('my', my, name='my'),
]
