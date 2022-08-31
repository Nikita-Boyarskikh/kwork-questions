from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
