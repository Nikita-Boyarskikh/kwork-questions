from django.urls import path

from rules.views import index

app_name = 'rules'
urlpatterns = [
    path('', index, name='index'),
]
