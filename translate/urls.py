from django.urls import path

from translate.views import translate_text

app_name = 'translate'
urlpatterns = [
    path('', translate_text, name='translate'),
]
