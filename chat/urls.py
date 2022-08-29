from django.urls import path

from chat.views import index

app_name = 'chat'
urlpatterns = [
    path('', index, name='index'),
]
