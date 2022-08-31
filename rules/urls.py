from django.urls import path

from rules.views import index, accept_agreement

app_name = 'rules'
urlpatterns = [
    path('', index, name='index'),
    path('accept_agreement', accept_agreement, name='accept_agreement'),
]
