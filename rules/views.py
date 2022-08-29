from django.shortcuts import render

from languages.models import Language
from rules.models import Rule


def index(request):
    return render(request, 'rules/list.html', {
        'object_list': Rule.objects.filter(language=Language.get_for_request(request)),
    })
