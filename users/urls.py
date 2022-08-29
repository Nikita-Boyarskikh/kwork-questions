from django.urls import path

from users.views import me

app_name = 'users'
urlpatterns = [
    path('', me, name='me'),
]
