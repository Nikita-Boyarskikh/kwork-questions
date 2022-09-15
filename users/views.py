from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from languages.models import Language
from users.forms import ChangeAvatarForm


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ChangeAvatarForm
    template_name = 'users/me.html'

    def get_success_url(self):
        return reverse('users:me')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs


def change_preferred_language(request, lang):
    if request.user.is_authenticated:
        request.user.preferred_language = Language.objects.get(id=lang)
        request.user.save()
    else:
        request.session['preferred_language'] = lang
    return redirect(request.GET.get('next', 'index'))


me = UpdateUserView.as_view()
