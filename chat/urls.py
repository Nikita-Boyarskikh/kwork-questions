from django.urls import path

from chat.views import index, create

app_name = 'chat'
urlpatterns = [
    path('', index, name='index'),
    path('create', create, name='create'),
]
