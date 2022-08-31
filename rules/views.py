from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from languages.models import Language
from rules.models import Rule


def index(request):
    return render(request, 'rules/list.html', {
        'object_list': Rule.objects.filter(language=Language.get_for_request(request)),
    })


@login_required
def accept_agreement(request):
    request.user.is_user_agreement_accepted = True
    request.user.save()
    return redirect('rules:index')
