from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from languages.models import Language
from users.forms import ChangeAvatarForm


@login_required
@render_to('users/me.html')  # TODO refactor other
def me(request):
    form = ChangeAvatarForm(instance=request.user)
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            form = ChangeAvatarForm(instance=request.user)
    return {'form': form}


def change_preferred_language(request, lang):
    if request.user.is_authenticated:
        request.user.preferred_language = Language.objects.get(id=lang)
        request.user.save()
    else:
        request.session['preferred_language'] = lang
    return redirect(request.GET.get('next', 'index'))
