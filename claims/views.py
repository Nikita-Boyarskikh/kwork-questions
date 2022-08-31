from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from answers.models import Answer
from claims.forms import ClaimCreateForm
from claims.models import Claim


@login_required
def create(request, answer_id):
    claim = Claim(
        author=request.user,
        object_id=answer_id,
        content_type=Answer.content_type,
    )
    form = ClaimCreateForm(instance=claim)

    if request.method == 'POST':
        form = ClaimCreateForm(request.POST, instance=claim)
        if form.is_valid():
            claim = form.save()
            question = claim.claimed_object.question
            return redirect('answers:detail', country_id=question.country_id, question_id=question.id, pk=answer_id)

    return render(request, 'claims/create.html', {
        'form': form,
    })
