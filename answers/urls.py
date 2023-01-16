from django.urls import path, include

from answers.views import create, index, my, full_text

app_name = 'answers'
urlpatterns = [
    path('<int:question_id>/', include([
        path('', index, name='index'),
        path('create', create, name='create'),
        path('<int:pk>', full_text, name='detail'),
    ])),
    path('my', my, name='my'),
]
