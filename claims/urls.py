from django.urls import path

from claims.views import create

app_name = 'claims'
urlpatterns = [
    path('<str:content_type>/<int:object_id>', create, name='create'),
]
