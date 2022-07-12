from django.conf import settings
from django.shortcuts import render


def list_view(answer):
    return answer[:settings.ANSWER_PREVIEW_TEXT_SIZE]
