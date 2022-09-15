from django.urls import path

from users.views import me, change_preferred_language

app_name = 'users'
urlpatterns = [
    path('', me, name='me'),
    path('<str:lang>', change_preferred_language, name='change_preferred_language'),
]
