from django.urls import path, include

from answers.views import create, index, my, detail

app_name = 'answers'
urlpatterns = [
    path('<int:question_id>/', include([
        path('', index, name='index'),
        path('create', create, name='create'),
        path('<int:pk>', detail, name='detail'),
    ])),
    path('my', my, name='my'),
]
