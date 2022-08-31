from django.urls import path

from claims.views import create

app_name = 'claims'
urlpatterns = [
    path('<int:answer_id>', create, name='create'),
]
