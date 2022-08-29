from django.urls import path

from questions.views import create, closed, publish, answered, my, my_answered, index

app_name = 'questions'
urlpatterns = [
    path('', index, name='index'),
    path('my', my, name='my'),
    path('my-voting', my_answered, name='my_voting'),
    path('voting', answered, name='voting'),
    path('closed', closed, name='closed'),
    path('create', create, name='create'),
    path('<int:pk>/publish', publish, name='publish'),
]
