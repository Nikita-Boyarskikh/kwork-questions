from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import ListView

from languages.models import Language
from rules.models import Rule


class RuleListView(ListView):
    model = Rule
    template_name = 'rules/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(language=Language.get_for_request(self.request))


@login_required
def accept_agreement(request):
    request.user.is_user_agreement_accepted = True
    request.user.save()
    return redirect('rules:index')


index = RuleListView.as_view()
