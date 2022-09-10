from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from languages.models import Language
from users.forms import ChangeAvatarForm


@login_required
def me(request):
    form = ChangeAvatarForm(instance=request.user)
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'users/me.html', {
        'form': form,
    })


def change_preferred_language(request, lang):
    if request.user.is_authenticated:
        request.user.preferred_language = Language.objects.get(id=lang)
        request.user.save()
    else:
        request.session['preferred_language'] = lang
    return redirect(request.GET.get('next', 'index'))
